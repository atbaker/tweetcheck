"""
Django settings for twitter_approver project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'test-key-not-for-prod'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
)

LOCAL_APPS = (
    'core',
    'twitter',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR'),
        'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT'),
    }
}

REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR')
REDIS_PORT = os.environ.get('REDIS_PORT_6379_TCP_PORT')

AUTH_USER_MODEL = 'core.TweetCheckUser'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Template settings
TEMPLATE_DIRS = (
    join(BASE_DIR, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

STATICFILES_DIRS = (
    join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

# Media
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = join(BASE_DIR, 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = '/#/'

# REST Framework
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Project-specific settings
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
