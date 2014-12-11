from celery import Celery

from django.conf import settings

# Use database 1 for the message broker
BROKER_URL = 'redis://{0}:{1}/1'.format(settings.REDIS_HOST, settings.REDIS_PORT)

app = Celery('tweetcheck', broker=BROKER_URL)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
