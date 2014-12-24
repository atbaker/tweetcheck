'''
Production Configurations
'''

from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.tweetcheck.com']

# REST Framework (remove SessionAuthentication)
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
  'rest_framework.authentication.TokenAuthentication',
)
