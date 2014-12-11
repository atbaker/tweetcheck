from celery import shared_task

from .models import Tweet

@shared_task
def publish_later(tweet_id):
    print('FOOOO {0}'.format(tweet_id))

