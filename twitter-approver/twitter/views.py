from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth1Session
from rest_framework import viewsets

import json

from .models import Tweet, Handle
from .serializers import TweetSerializer, HandleSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

class HandleViewSet(viewsets.ModelViewSet):
    queryset = Handle.objects.all()
    serializer_class = HandleSerializer

def get_request_token(request):
    request_token_url = 'https://api.twitter.com/oauth/request_token'

    oauth = OAuth1Session(settings.TWITTER_API_KEY, client_secret=settings.TWITTER_API_SECRET)
    fetch_response = oauth.fetch_request_token(request_token_url)

    request.session['resource_owner_key'] = fetch_response.get('oauth_token')
    request.session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)

    return HttpResponse(json.dumps({'authorizationUrl': authorization_url}))

def callback(request):
    # http://www.tweetcheck.com/callback?oauth_token=oxS47MU7v40oP3hWdGEBFw8KBe8yAOxk&oauth_verifier=QfF3IavGlsFYrwpkQxHG0CxlCIAdZqvj
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

    Handle.objects.get_or_create(
        screen_name=screen_name,
        # organization=request.user.organization,
        access_token=resource_owner_key,
        token_secret=resource_owner_secret)

    return redirect('/')
