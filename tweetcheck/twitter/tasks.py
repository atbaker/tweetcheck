from celery import shared_task

@shared_task
def publish_later(tweet_id):
    from .models import Tweet

    tweet = Tweet.objects.get(pk=tweet_id)
    tweet.body = 'I AM UPDATED'

    tweet.save()
