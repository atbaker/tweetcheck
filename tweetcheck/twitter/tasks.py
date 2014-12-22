from celery import shared_task

import arrow

@shared_task(bind=True)
def publish_later(self, tweet_id):
    """Publishes a tweet in the future"""
    from .models import Tweet

    tweet = Tweet.objects.get(pk=tweet_id)

    tweet_eta = arrow.get(tweet.eta)
    task_eta = arrow.get(self.request.eta)

    # Don't publish if the Tweet has been published
    # or its scheduled time has changed since
    # this task was submitted
    if tweet.twitter_id or tweet_eta != task_eta:
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
