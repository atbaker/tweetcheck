from rest_framework import serializers
from .models import Tweet, Handle


class TweetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tweet
        fields = ('url', 'id', 'handle', 'body', 'approved',)

class HandleSerializer(serializers.HyperlinkedModelSerializer):
    name_with_organization = serializers.CharField(source='__unicode__', read_only=True)
    organization = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Handle
        fields = ('url', 'id', 'screen_name', 'organization', 'name_with_organization')
