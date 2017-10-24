import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.environ.setdefault('CV_HOST_DIR', BASE_DIR)
os.environ.setdefault('CV_LOGS_DIR', os.path.join(BASE_DIR, 'logs'))
os.environ.setdefault('CV_ROOT_URL', 'http://0.0.0.0:8000')


from django_project.settings_base import *  # noqa


SECRET_KEY = 'devel key'

ALLOWED_HOSTS = ['*']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'common': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}
