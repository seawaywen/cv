import os

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured('Must set env variable:{}'.format(var_name))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_DIR = os.path.join(BASE_DIR, 'src')
_HOST_DIR = os.path.join(BASE_DIR, os.path.pardir, os.path.pardir)
HOST_DIR = os.path.abspath(os.getenv('MEMODIR_HOST_DIR', _HOST_DIR))
_LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir)) + '-logs'
LOG_DIR = os.path.abspath(os.getenv('MEMODIR_LOG_DIR', _LOG_DIR))

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

"""
print('BASE_DIR:{}'.format(BASE_DIR))
print('SRC_DIR:{}'.format(SRC_DIR))
print('HOST_DIR:{}'.format(HOST_DIR))
print('LOG_DIR:{}'.format(_LOG_DIR))
"""
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

DB_HOST = os.environ.get('DB_SERVICE', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'memodir')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '')
GOOGLE_TAG_MANAGER_ID = os.environ.get('GOOGLE_TAG_MANAGER_ID', None)

_SECRET_KEY = '_m#d24ll8(hxv#wn(+@t3rxw9$3w172l(r_v)anwk(dj8!55b6'
SECRET_KEY = os.environ.get('SECRET_KEY', _SECRET_KEY)

ALLOWED_HOSTS = []

#CRISPY_TEMPLATE_PACK = 'uni_form'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'webpack_loader',
    'crispy_forms',
    'tinymce',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    'myaccount',
    'profile',
    'resume',
]



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'myaccount.authentication.EmailAuthBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

SIGNUP_OPEN = True
EMAIL_DEFAULT_FROM = 'admin@memodir.com'
ACCOUNT_ACTIVATION_HOURS = 1

LOGIN_URL = "signin"
LOGOUT_URL = "signout"
LOGIN_REDIRECT_URL = reverse_lazy('profile')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'resume.context_processors.google_tag_manager_setup',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 600,
        #'TIME_ZONE': 'UTC',
        'HOST': DB_HOST,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'PORT': DB_PORT,
        'TEST': {
            'NAME': None,
            'MIRROR': None,
            'CHARSET': None,
            'COLLATION': None,
        },
        'OPTIONS': {},
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('zh-hans', _('Chinese')),
]


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [
    ('dist', os.path.join(BASE_DIR, 'static_src', 'dist')),
    ('css', os.path.join(BASE_DIR, 'static', 'css')),
    ('images', os.path.join(BASE_DIR, 'static', 'images')),
    ('js', os.path.join(BASE_DIR, 'static', 'js')),
    ('templates', os.path.join(BASE_DIR, 'static', 'templates')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_ROOT = os.path.join(HOST_DIR, 'www', 'media')
MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            os.path.join(BASE_DIR, 'static', 'templates'),
        ),
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages']
        }
    },
]

#AUTH_USER_MODEL = "profile.UserProfile"

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': os.path.join(
            BASE_DIR, 'static_src/dist/webpack-stats.json'),
    }
}

if not DEBUG:
    WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = os.path.join(
        BASE_DIR, 'staticfiles/dist/webpack-stats.json')


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

RESERVED_PROFILE_NAMESPACE_LIST = (
    'memodir-test-namespace'
)

IMAGE_UPLOAD_TO = 'images/%Y/%m'
PROFILE_PHOTO_UPLOAD_TO = 'profile_photo/%Y/%m'
THUMBNAIL_UPLOAD_TO = 'thumbnails/%Y/%m'
THUMBNAIL_PROFILE_PHOTO_UPLOAD_TO = 'thumbnails/profile_photo/%Y/%m'


class LevelFilter(object):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        if self.level == record.levelname:
            return 1
        return 0


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [logger: %(name)s] [line %(lineno)s, in %(module)s::%(funcName)s] %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'standard': {
            'format': "[%(asctime)s] [%(levelname)s] %(name)s[%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'OnlyDebug': {
            '()': LevelFilter,
            'level': 'DEBUG'
        },
        'OnlyInfo': {
            '()': LevelFilter,
            'level': 'INFO'
        },
        'OnlyWarning': {
            '()': LevelFilter,
            'level': 'WARNING'
        },
        'OnlyError': {
            '()': LevelFilter,
            'level': 'ERROR'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'all.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debug_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'verbose',
            'filters': ['OnlyDebug']
        },
        'info_log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
            'filters': ['OnlyInfo']
        },
        'warn_log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'warning.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
            'filters': ['OnlyWarning']
        },
        'error_log_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'standard',
            'filters': ['OnlyError']
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        }
    }
}


SITE_ID = 1

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_buttons1': '''bold, italic, underline, strikethrough, |,
                               forecolor, backcolor, |,
                               justifyleft, justifycenter, justifyright,
                               justifyfull, fontselect, fontsizeselect,
                               fullscreen, code''',
    'theme_advanced_buttons2': '''bullist, numlist, |, outdent, indent,
                               blockquote, |, undo, redo, |, link, unlink, |,
                               ''',
    'theme_advanced_buttons3': '',
    'relative_urls': False, # default value
    'width': '100%',
    'height': 300
}
