'''
Production Configurations
'''

from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.tweetcheck.com']
