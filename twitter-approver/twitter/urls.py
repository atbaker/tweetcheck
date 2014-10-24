from django.conf.urls import url, patterns, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'tweets', views.TweetViewSet)
router.register(r'handles', views.HandleViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('twitter.views',
    url(r'^$', TemplateView.as_view(template_name="base.html")),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^auth/request$', 'get_request_token'),
    url(r'^auth/callback$', 'callback'),

)
