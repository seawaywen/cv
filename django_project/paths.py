#! /usr/bin/env python

import sys
import os

PATHS = [
    # src and config
    '.',
    'src',
]

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))

LOCAL_SETTINGS_DIR = os.path.abspath(
    os.path.join(PROJECT_ROOT_DIR, os.pardir, 'local_config'))
LOCAL_SETTINGS_PATH = os.path.join(LOCAL_SETTINGS_DIR, 'settings.py')


def get_paths(paths):
    # only include a path if not already in sys.path to avoid duplication of
    # paths when using code reloading
    path_set = set(sys.path)
    for p in paths:
        path = os.path.abspath(os.path.join(PROJECT_ROOT_DIR, p))
        if path not in path_set:
            yield path


def setup_paths():
    sys.path = list(get_paths(PATHS)) + sys.path
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')


if __name__ == '__main__':
    # For use in shell scripting
    # e.g. $(python paths.py)
    print("export PYTHONPATH=%s" % ":".join(get_paths(PATHS)))
    print("export DJANGO_SETTINGS_MODULE=django_project.settings")
