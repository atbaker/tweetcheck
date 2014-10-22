'''
Production Configurations
'''

from .common import Common


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
