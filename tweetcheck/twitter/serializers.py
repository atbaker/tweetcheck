from rest_framework import serializers
from .models import Tweet, Handle


class HandleSerializer(serializers.ModelSerializer):
    name_with_organization = serializers.CharField(source='__unicode__', read_only=True)
    organization = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Handle
        fields = ('id', 'screen_name', 'organization', 'name_with_organization',
            'user_id', 'name', 'profile_image_url')


class TweetSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_short_name', read_only=True)
    last_editor = serializers.CharField(source='last_editor.get_short_name', read_only=True)

    class Meta:
        model = Tweet
        fields = ('id', 'handle', 'body', 'status', 'author', 'created', 'last_editor', 'last_modified')
