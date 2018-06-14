import os
import os.path

from setuptools import setup, find_packages


def find_packages_data(start_dir):
    packages = {}
    for package_name in os.listdir(start_dir):
        package_dir = os.path.join(start_dir, package_name)
        if os.path.exists(os.path.join(package_dir, '__init__.py')):
            files = []
            packages[package_name] = files
            for dirpath, dirnames, filenames in os.walk(package_dir):
                dirpath = dirpath[len(package_dir) + 1:]
                for filename in filenames:
                    ext = os.path.splitext(filename)[1]
                    if ext not in ('.py', '.pyc', '.pyo'):
                        file_path = os.path.join(dirpath, filename)
                        full_file_path = os.path.join(package_dir, file_path)
                        if os.path.isfile(full_file_path):
                            files.append(file_path)
    return packages


setup(
    name = "memodir.cv",
    version = "0.01",

    author = "memodir.com",
    author_email = "kelvin@memodir.com",
    zip_safe = False,

    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data = find_packages_data('src'),
)
