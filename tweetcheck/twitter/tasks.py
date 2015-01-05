from celery import shared_task
from django.conf import settings

import arrow
import redis

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

@shared_task(bind=True)
def publish_later(self, tweet_id):
    """Publishes a tweet in the future"""
    from .models import Tweet

    tweet = Tweet.objects.get(pk=tweet_id)

    tweet_eta = arrow.get(tweet.eta)
    task_eta = arrow.get(self.request.eta)

    # Don't publish if:
    # - The Tweet has been published already
    # - Its scheduled time has changed since this task was submitted
    # - its status has changed
    if tweet.twitter_id or tweet_eta != task_eta or tweet.status != Tweet.SCHEDULED:
      return

    tweet.twitter_id = tweet.publish()
    tweet.save(from_scheduler=True)

@shared_task
def check_eta(tweet_id):
    """Removes a tweet's eta if its ETA is now in the past"""
    from .models import Tweet

    tweet = Tweet.objects.get(pk=tweet_id)

    if tweet.status != Tweet.PENDING:
      return

    tweet_eta = arrow.get(tweet.eta)
    if tweet_eta <= arrow.utcnow():
      tweet.eta = None
      tweet.save()

@shared_task
def publish_counts(org_id):
    """Publishes the latest counts of pending and scheduled tweets to redis"""
    from .models import Tweet

    org_tweets = Tweet.objects.filter(handle__organization__id=org_id)

    pending = org_tweets.filter(status=Tweet.PENDING).count()
    r.publish('{0}-pending'.format(org_id), pending)

    scheduled = org_tweets.filter(status=Tweet.SCHEDULED).count()
    r.publish('{0}-scheduled'.format(org_id), scheduled)
