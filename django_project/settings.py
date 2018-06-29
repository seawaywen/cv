import os

os.environ.setdefault('CV_ROOT_URL', 'http://cv-memodir:8000')

from django_project.settings_devel import *

TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
