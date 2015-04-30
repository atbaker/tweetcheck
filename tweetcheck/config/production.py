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
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
