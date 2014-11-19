from rest_framework import serializers
from .models import Tweet, Handle


class HandleSerializer(serializers.HyperlinkedModelSerializer):
    name_with_organization = serializers.CharField(source='__unicode__', read_only=True)
    organization = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Handle
        fields = ('url', 'id', 'screen_name', 'organization', 'name_with_organization')


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    screen_name = serializers.CharField(source='handle.screen_name', read_only=True)

    class Meta:
        model = Tweet
        fields = ('url', 'id', 'handle', 'screen_name', 'body', 'approved',)
