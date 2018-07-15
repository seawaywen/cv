import os

os.environ.setdefault('CV_ROOT_URL', 'http://cv-memodir:8000')

from django_project.settings_devel import *

TEMPLATE_DEBUG = True

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True


