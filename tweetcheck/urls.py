from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Not sure if I need api-auth
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),

    url(r'^auth/request$', 'twitter.views.get_request_token'),
    url(r'^auth/callback$', 'twitter.views.callback'),

    url(r'^', include('twitter.urls')),
)
