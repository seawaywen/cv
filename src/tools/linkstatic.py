import os

from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.core.management.base import CommandError


class Command(collectstatic.Command):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        # Asset files and directories used to generate make dependencies
        self.asset_files = []
        self.asset_parents = []

    def collect(self):
        """Wrap base class 'collect' to generate make dependencies."""
        ret = super(Command, self).collect()
        dependencies = set(self.asset_files + self.asset_parents)
        # The rule template makes 'collectstatic.deps.mk' depends on any file
        # or folder in the asset hierarchy so that the assets are
        # collected when any of them change (and the dependencies are rebuilt
        # to track those changes).
        rule = ('collectstatic.deps.mk: {}\n')
        with open('collectstatic.deps.mk', 'w') as f:
            for dep in sorted(dependencies):
                if dep.startswith('static_src'):
                    continue
                f.write(rule.format(dep))
            # 'static_src/dist' is special: its content is under version
            # control and produced by gulp. As such, directories can disappear
            # when the branch is updated which fools make.
            f.write(rule.format('$(shell find static_src/dist)'))
        return ret

    def intercept_source_file_handling(self, path, prefixed_path,
                                       source_storage):
        """Keep track of an asset source file and its parents.

        For a given file in the asset collection, establish the list of make
        dependencies that needs to be tracked. It's the file itself plus any of
        its parent directories so additions/deletions in the hierarchy triggers
        the whole collection.

        The de-duplication is done in collect once all files has been
        collected.

        """
        full_path = source_storage.path(path)
        relpath = os.path.relpath(full_path, settings.BASE_DIR)
        self.asset_files.append(relpath)

    def copy_file(self, path, prefixed_path, source_storage):
        self.intercept_source_file_handling(
            path, prefixed_path, source_storage)
        return super(Command, self).copy_file(path, prefixed_path,
                                              source_storage)

    def link_file(self, path, prefixed_path, source_storage):
        """
        Attempt to link ``path``
        """
        self.intercept_source_file_handling(
            path, prefixed_path, source_storage)
        # Skip this file if it was already copied earlier
        if prefixed_path in self.symlinked_files:
            return self.log("Skipping '%s' (already linked earlier)" % path)
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally link the file
        if self.dry_run:
            self.log("Pretending to link '%s'" % source_path, level=1)
        else:
            self.log("Linking '%s'" % source_path, level=1)
            full_path = self.storage.path(prefixed_path)
            dir_path = os.path.dirname(full_path)
            try:
                os.makedirs(dir_path)
            except OSError:
                pass

            relpath = os.path.relpath(source_path, dir_path)

            try:
                if os.path.lexists(full_path):
                    os.unlink(full_path)
                os.symlink(relpath, full_path)
            except AttributeError:
                import platform
                raise CommandError(
                    "Symlinking is not supported by Python %s."
                    % platform.python_version())
            except NotImplementedError:
                import platform
                raise CommandError("Symlinking is not supported in this "
                                   "platform (%s)." % platform.platform())
            except OSError as e:
                raise CommandError(e)
        if prefixed_path not in self.symlinked_files:
            self.symlinked_files.append(prefixed_path)
