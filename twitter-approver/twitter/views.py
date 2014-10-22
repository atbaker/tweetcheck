from django.conf import settings
from rest_framework import viewsets

from .models import Tweet
from .serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents tweets.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

def get_my_tweets(request):
    import requests
    from requests_oauthlib import OAuth1

    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET,
                  settings.ATB_ACCESS_TOKEN, settings.ATB_TOKEN_SECRET)
    response = requests.get(url, auth=auth)
    import pdb; pdb.set_trace();


