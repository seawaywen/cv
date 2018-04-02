import os
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


print('BASE_DIR:{}'.format(BASE_DIR))
print('SRC_DIR:{}'.format(SRC_DIR))
print('HOST_DIR:{}'.format(HOST_DIR))
print('LOG_DIR:{}'.format(_LOG_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_m#d24ll8(hxv#wn(+@t3rxw9$3w172l(r_v)anwk(dj8!55b6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    
    'crispy_forms',
    'webpack_loader',
    
    'resume',
]

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
        'NAME': 'memodir',
        #'TIME_ZONE': 'UTC',
        'PORT': '',
        'HOST': 'localhost',
        'USER': 'postgres',
        'TEST': {
            'NAME': None,
            'MIRROR': None,
            'CHARSET': None,
            'COLLATION': None,
        },
        'PASSWORD': '',
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

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en-us', _('English')),
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
            #os.path.join(BASE_DIR, "static_src/dist/templates"),
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

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': os.path.join(BASE_DIR, 'static_src/webpack-stats.json'),
    }
}

RESERVED_PROFILE_NAMESPACE_LIST = (
    'memodir-test-namespace'
)

IMAGE_UPLOAD_TO = 'images/%Y/%m'
PROFILE_PHOTO_UPLOAD_TO = 'profile_photo/%Y/%m'
THUMBNAIL_UPLOAD_TO = 'thumbnails/%Y/%m'
THUMBNAIL_PROFILE_PHOTO_UPLOAD_TO = 'thumbnails/profile_photo/%Y/%m' 



