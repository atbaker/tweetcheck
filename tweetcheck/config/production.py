'''
Production Configurations
'''

from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allowing all hosts since we'll run on Docker
ALLOWED_HOSTS = ['*']

# CORS
CORS_ORIGIN_WHITELIST = (
    'tweetcheck.com',
)

# REST Framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
  'rest_framework.authentication.TokenAuthentication',
)

# Opbeat
THIRD_PARTY_APPS += (
    'opbeat.contrib.django',
)

OPBEAT = {
    "ORGANIZATION_ID": "a6501252831542bbac32b8970f04d9a6",
    "APP_ID": "abaa6eeecc",
    "SECRET_TOKEN": os.environ.get('OPBEAT_SECRET_TOKEN')
}

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
) + MIDDLEWARE_CLASSES
