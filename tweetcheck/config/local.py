'''
Local Configurations

- Runs in Debug mode
- Uses console backend for emails
- Use Django Debug Toolbar
'''
from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

# CORS
CORS_ORIGIN_ALLOW_ALL = True
