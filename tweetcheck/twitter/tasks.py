from celery import shared_task

import arrow

@shared_task(bind=True)
def publish_later(self, tweet_id):
    from .models import Tweet

    tweet = Tweet.objects.get(pk=tweet_id)

    tweet_eta = arrow.get(tweet.eta)
    task_eta = arrow.get(self.request.eta)

    # Don't publish if the Tweet has been published
    # or its scheduled time has changed since
    # this task was submitted
    if tweet.twitter_id or tweet_eta != task_eta:
      tweet.body = '{0} - {1}'.format(tweet.eta, task_eta)
      tweet.status = Tweet.PENDING
      tweet.save()
      return

    tweet.twitter_id = tweet.publish()
    tweet.save(from_scheduler=True)
