from rest_framework import viewsets

from .models import TweetCheckUser, Action
from .serializers import UserSerializer, ActionSerializer

class OrganizationQuerysetMixin(object):
    def get_queryset(self):
        return self.model.objects.filter(organization=self.request.user.organization)

class UserViewSet(OrganizationQuerysetMixin, viewsets.ModelViewSet):
    model = TweetCheckUser
    queryset = TweetCheckUser.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        return queryset.filter(is_active=True)

class ActionViewSet(OrganizationQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    model = Action
    serializer_class = ActionSerializer

    def get_queryset(self):
        queryset = super(ActionViewSet, self).get_queryset()

        tweet_id = self.request.QUERY_PARAMS.get('tweet_id', None)
        if tweet_id is not None:
            queryset = queryset.filter(tweet=tweet_id)

        return queryset
