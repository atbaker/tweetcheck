from rest_framework import serializers
from .models import TweetCheckUser, Action


class UserSerializer(serializers.ModelSerializer):
    email_without_domain = serializers.CharField(source='get_short_name', read_only=True)
    organization = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = TweetCheckUser
        fields = ('id', 'email', 'email_without_domain', 'organization', 'is_approver')

class ActionSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.get_short_name')
    action = serializers.CharField(source='get_action_display')

    class Meta:
        model = Action
        fields = ('id', 'organization', 'actor', 'action', 'tweet', 'body', 'timestamp')
