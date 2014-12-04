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
