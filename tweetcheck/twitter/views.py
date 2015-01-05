from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth1Session
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import json
import urllib.parse

from .models import Tweet, Handle
from .permissions import IsApprover
from .serializers import TweetSerializer, HandleSerializer
from core.views import OrganizationQuerysetMixin


class TweetViewSet(OrganizationQuerysetMixin, viewsets.ModelViewSet):
    model = Tweet
    permission_classes = (IsAuthenticated,IsApprover)
    serializer_class = TweetSerializer

    def get_queryset(self):
        queryset = super(TweetViewSet, self).get_queryset()
        queryset.annotate(null_eta=Count('eta')).order_by('null_eta', 'eta', 'created')

        query_params = self.request.QUERY_PARAMS
        status = query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)

        since_id = query_params.get('since_id', None)
        if since_id is not None:
            queryset = queryset.filter(id__gt=since_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, last_editor=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_editor=self.request.user)

class HandleViewSet(OrganizationQuerysetMixin, viewsets.ModelViewSet):
    model = Handle
    serializer_class = HandleSerializer

class ListCounts(APIView):
    def get(self, request, format=None):
        counts = Tweet.get_counts(self.request.user.organization.id)
        return Response(counts)

def get_request_token(request):
    request_token_url = 'https://api.twitter.com/oauth/request_token'

    oauth = OAuth1Session(settings.TWITTER_API_KEY, client_secret=settings.TWITTER_API_SECRET)
    fetch_response = oauth.fetch_request_token(request_token_url)

    request.session['resource_owner_key'] = fetch_response.get('oauth_token')
    request.session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url, force_login='true')

    return HttpResponse(json.dumps({'authorizationUrl': authorization_url}))

def callback(request):
    oauth = OAuth1Session(settings.TWITTER_API_KEY, client_secret=settings.TWITTER_API_SECRET)
    oauth_response = oauth.parse_authorization_response(request.get_full_path())
    verifier = oauth_response.get('oauth_verifier')

    resource_owner_key = request.session['resource_owner_key']
    resource_owner_secret = request.session['resource_owner_secret']

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(settings.TWITTER_API_KEY,
                          client_secret=settings.TWITTER_API_SECRET,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    screen_name = oauth_tokens.get('screen_name')

    user_token_key = urllib.parse.unquote(request.COOKIES['token']).strip('"')
    user_token = Token.objects.get(key=user_token_key)

    Handle.objects.update_or_create(
        screen_name=screen_name,
        defaults={
            'organization': user_token.user.organization,
            'access_token': resource_owner_key,
            'token_secret': resource_owner_secret
        }
    )

    return redirect('/dashboard/review')
