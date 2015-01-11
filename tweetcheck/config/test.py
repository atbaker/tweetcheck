'''
Test Configuration
'''

from .common import *

DEBUG = True
TEMPLATE_DEBUG = True

# Timezone
USE_TZ = False

# Redis
REDIS_DB = 9

# Celery
CELERY_ALWAYS_EAGER = True

# CORS
CORS_ORIGIN_ALLOW_ALL = True
