from rest_framework import viewsets

from .models import TweetCheckUser, Action
from .serializers import UserSerializer, ActionSerializer

class OrganizationQuerysetMixin(object):
    def get_queryset(self):
        return self.model.objects.filter(organization=self.request.user.organization)

class UserViewSet(OrganizationQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    model = TweetCheckUser
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()

        token = self.request.QUERY_PARAMS.get('token', None)
        if token is not None:
            queryset = queryset.filter(auth_token__key=token)

        return queryset

class ActionViewSet(OrganizationQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    model = Action
    serializer_class = ActionSerializer
    paginate_by = 10

    def get_queryset(self):
        queryset = super(ActionViewSet, self).get_queryset()

        tweet_id = self.request.QUERY_PARAMS.get('tweet_id', None)
        if tweet_id is not None:
            queryset = queryset.filter(tweet=tweet_id)

        return queryset
