from rest_framework import viewsets

from .models import TweetCheckUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = TweetCheckUser.objects.filter(is_active=True)
    serializer_class = UserSerializer
