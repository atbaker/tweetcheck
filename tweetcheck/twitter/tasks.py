from celery import shared_task

@shared_task(bind=True)
def publish_later(self, tweet_id):
    from .models import Tweet

    tweet = Tweet.objects.get(pk=tweet_id)
    tweet.body = self.request.id

    tweet.save()
