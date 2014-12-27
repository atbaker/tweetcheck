'''
Local Configurations

- Runs in Debug mode
- Uses console backend for emails
- Use Django Debug Toolbar
'''
from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar',)

# CORS
CORS_ORIGIN_ALLOW_ALL = True
