from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'tweets', views.TweetViewSet)
router.register(r'handles', views.HandleViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('twitter.views',
    url(r'^api/', include(router.urls)),
    url(r'^$', login_required(TemplateView.as_view(template_name="ng-base.html"))),
)
