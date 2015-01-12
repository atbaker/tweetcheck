from rest_framework import serializers
from .models import TweetCheckUser, Device, Action


class UserSerializer(serializers.ModelSerializer):
    email_without_domain = serializers.CharField(source='get_short_name', read_only=True)

    class Meta:
        model = TweetCheckUser
        fields = ('id', 'email', 'email_without_domain', 'organization', 'is_approver')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('token', 'user')

class ActionSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.get_short_name')
    action = serializers.CharField(source='get_action_display')
    handle = serializers.IntegerField(source='tweet.handle.id')

    class Meta:
        model = Action
        fields = ('id', 'organization', 'handle', 'actor', 'action', 'tweet', 'body', 'timestamp')
