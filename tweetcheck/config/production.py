'''
Production Configurations
'''

from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.tweetcheck.com']

# REST Framework
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
  'rest_framework.authentication.TokenAuthentication',
)
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
