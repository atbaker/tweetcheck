from rest_framework import serializers
from .models import Tweet, Handle


class TweetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tweet
        fields = ('url', 'id', 'handle', 'body', 'approved',)

class HandleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Handle
        fields = ('url', 'id', 'screen_name',)
