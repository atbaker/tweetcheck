from rest_framework import serializers
from .models import TweetCheckUser


class UserSerializer(serializers.ModelSerializer):
    email_without_domain = serializers.CharField(source='get_short_name', read_only=True)
    organization = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = TweetCheckUser
        fields = ('id', 'email', 'email_without_domain', 'organization', 'is_approver')
