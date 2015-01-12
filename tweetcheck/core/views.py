from rest_framework import viewsets

from .models import TweetCheckUser, Device, Action
from .serializers import UserSerializer, DeviceSerializer, ActionSerializer

class OrganizationQuerysetMixin(object):
    def get_queryset(self):
        if self.model.__name__ == 'Tweet':
            return self.model.objects.filter(handle__organization=self.request.user.organization)
        elif self.model.__name__ == 'Device':
            return self.model.objects.filter(user__organization=self.request.user.organization)
        else:
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeviceViewSet(OrganizationQuerysetMixin, viewsets.ModelViewSet):
    model = Device
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = super(DeviceViewSet, self).get_queryset()

        token = self.request.QUERY_PARAMS.get('token', None)
        if token is not None:
            queryset = queryset.filter(token=token)

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
