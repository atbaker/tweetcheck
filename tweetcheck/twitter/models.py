from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from requests_oauthlib import OAuth1

import redis
import requests

from core.models import Action

class Handle(models.Model):
    screen_name = models.CharField(max_length=50)
    organization = models.ForeignKey('core.Organization')
    access_token = models.CharField(max_length=100)
    token_secret = models.CharField(max_length=100)

    # Other Handle details - updated regularly
    user_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    profile_image_url = models.URLField(blank=True)

    class Meta:
        ordering = ('screen_name',)

    def __str__(self):
        return '{0} (@{1})'.format(self.name, self.screen_name)

    def update_details(self):
        url = 'https://api.twitter.com/1.1/users/show.json'
        auth = OAuth1(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET,
                  self.access_token, self.token_secret)
        payload = {
            'screen_name': self.screen_name
        }

        response = requests.get(url, auth=auth, params=payload)
        details = response.json()

        self.user_id = details['id']
        self.name = details['name']
        self.profile_image_url = details['profile_image_url']

    def save(self, *args, **kwargs):
        self.update_details()
        super(Handle, self).save(*args, **kwargs)

def validate_tweet_body(value):
    short_url_length = 22
    short_url_length_https = 23

    remaining = 140
    split_body = value.split(' ')
    if len(split_body) > 1:
        remaining -= (len(split_body) - 1)

    for word in split_body:
        if word[0:7] == 'http://' and len(word) > short_url_length:
            remaining -= short_url_length
        elif word[0:8] == 'https://' and len(word) > short_url_length_https:
            remaining -= short_url_length_https
        else:
            remaining -= len(word)

    if remaining < 0:
        raise ValidationError('Tweet body is too long')

class Tweet(models.Model):
    PENDING = 0
    POSTED = 1
    REJECTED = -1

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (POSTED, 'posted'),
        (REJECTED, 'rejected')
    )

    handle = models.ForeignKey(Handle)
    body = models.CharField(max_length=250, validators=[validate_tweet_body])
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    twitter_id = models.CharField(max_length=25, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u'+')
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.body[:50])

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Tweet.objects.get(pk=self.pk)
            if (not original.status == Tweet.POSTED) and self.status == Tweet.POSTED:
                self.twitter_id = self.publish()
                activity_action = Action.POSTED
            elif (not original.status == Tweet.REJECTED) and self.status == Tweet.REJECTED:
                activity_action = Action.REJECTED
            else:
                activity_action = Action.EDITED
        else:
            if (self.status == Tweet.POSTED):
                self.twitter_id = self.publish()
                activity_action = Action.POSTED
            else:
                activity_action = Action.CREATED
        
        super(Tweet, self).save(*args, **kwargs)

        action = Action(action=activity_action,
            tweet=self)
        action.save()

        if activity_action == Action.CREATED:
            # Send a notification to redis for this org's channel
            r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
            r.publish(self.handle.organization.id, 'new')

    def publish(self):
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        auth = OAuth1(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET,
                  self.handle.access_token, self.handle.token_secret)
        payload = {
            'status': self.body,
        }

        # TO-DO: Add some error handling here
        response = requests.post(url, auth=auth, params=payload)
        data = response.json()

        return data['id_str']
