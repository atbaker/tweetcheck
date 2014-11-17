from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.authtoken.views import obtain_auth_token

from core.forms import LoginForm

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_auth_token),

    url(r'^auth/request$', 'get_request_token'),
    url(r'^auth/callback$', 'callback'),

    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html',
         'authentication_form': LoginForm
        }
    ),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),

    url(r'^', include('twitter.urls')),
)
