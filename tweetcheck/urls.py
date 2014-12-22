from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from core.views import UserViewSet, ActionViewSet
from twitter.views import TweetViewSet, HandleViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'actions', ActionViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'handles', HandleViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/request$', 'twitter.views.get_request_token'),
    url(r'^auth/callback$', 'twitter.views.callback'),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),
)
