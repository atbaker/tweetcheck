from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from requests_oauthlib import OAuth1

import redis
import requests

from config import celery_app
from core.models import Action
from .tasks import publish_later

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
    SCHEDULED = 3

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (POSTED, 'posted'),
        (REJECTED, 'rejected'),
        (SCHEDULED, 'scheduled')
    )

    handle = models.ForeignKey(Handle)
    body = models.CharField(max_length=250, validators=[validate_tweet_body])
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    eta = models.DateTimeField(blank=True, null=True)

    twitter_id = models.CharField(max_length=25, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u'+')
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('eta',)

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.body[:50])

    def save(self, *args, **kwargs):
        from_scheduler = kwargs.pop('from_scheduler', False)

        if from_scheduler:
            self.status = Tweet.POSTED
            activity_action = Action.POSTED
        else:
            if self.pk is not None:
                original = Tweet.objects.get(pk=self.pk)
                if (not original.status == Tweet.POSTED) and self.status == Tweet.POSTED:
                    self.twitter_id = self.publish()
                    activity_action = Action.POSTED
                elif (not original.status == Tweet.SCHEDULED) and self.status == Tweet.SCHEDULED:
                    activity_action = Action.SCHEDULED
                elif (not original.status == Tweet.REJECTED) and self.status == Tweet.REJECTED:
                    activity_action = Action.REJECTED
                else:
                    activity_action = Action.EDITED
            else:
                if self.status == Tweet.POSTED:
                    self.twitter_id = self.publish()
                    activity_action = Action.POSTED
                elif self.status == Tweet.SCHEDULED:
                    activity_action = Action.SCHEDULED
                else:
                    activity_action = Action.CREATED
        
        super(Tweet, self).save(*args, **kwargs)

        action = Action(action=activity_action,
            tweet=self)
        action.save()

        self.send_redis_message(activity_action)

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

    def send_redis_message(self, action):
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

        if action == Action.CREATED:
            message = 'new'
        else:
            message = self.id

        r.publish(self.handle.organization.id, message)

@receiver(post_save, sender=Tweet)
def update_scheduling(sender, instance, **kwargs):
    # If this tweet has a tweet_id, it has already been published
    if instance.twitter_id or instance.status != Tweet.SCHEDULED:
        return

    publish_later.apply_async(args=[instance.id], eta=instance.eta)
