from rest_framework import viewsets

from .models import Tweet
from .serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents tweets.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
