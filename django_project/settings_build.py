import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ['LOGS_DIR'] = os.path.abspath(os.path.join(BASE_DIR, 'logs'))


from django_project.settings import *  # noqa

SECRET_KEY = 'build key'

