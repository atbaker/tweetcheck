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

# Twitter API settings
TWITTER_API_KEY = '123'
TWITTER_API_SECRET = '456'
