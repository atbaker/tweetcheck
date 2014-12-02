from rest_framework import viewsets

from .models import TweetCheckUser, Action
from .serializers import UserSerializer, ActionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = TweetCheckUser.objects.filter(is_active=True)
    serializer_class = UserSerializer

class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
