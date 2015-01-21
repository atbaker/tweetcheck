'''
Local Configurations

- Runs in Debug mode
- Uses console backend for emails
'''
from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

# CORS
CORS_ORIGIN_ALLOW_ALL = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
