from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from requests_oauthlib import OAuth1

import redis
import requests

from core.models import TweetCheckUser, Action
from core.tasks import send_push_notifications
from .tasks import publish_later, check_eta, publish_counts

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

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
        self.profile_image_url = details['profile_image_url_https']

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
    created = models.DateTimeField(editable=False)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u'+')
    last_modified = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.body[:50])

    def save(self, *args, **kwargs):
        from_scheduler = kwargs.pop('from_scheduler', False)
        current_datetime = datetime.now()

        if from_scheduler:
            self.status = Tweet.POSTED
            self.last_editor = TweetCheckUser.objects.get(email='scheduler@tweetcheck.com')
            activity_action = Action.POSTED
        else:
            if self.pk is not None:
                original = Tweet.objects.get(pk=self.pk)
                if original.status != Tweet.POSTED and self.status == Tweet.POSTED:
                    self.twitter_id = self.publish()
                    activity_action = Action.POSTED
                elif original.status != Tweet.SCHEDULED and self.status == Tweet.SCHEDULED:
                    activity_action = Action.SCHEDULED
                elif original.status != Tweet.REJECTED and self.status == Tweet.REJECTED:
                    activity_action = Action.REJECTED
                else:
                    activity_action = Action.EDITED

                # If this tweet was already scheduled and its ETA has NOT changed,
                # note it in a special property so we can avoid duplicate celery tasks
                if original.status == Tweet.SCHEDULED and self.status == Tweet.SCHEDULED \
                and original.eta == self.eta:
                    self.eta_not_updated = True

            else:
                if self.status == Tweet.POSTED:
                    self.twitter_id = self.publish()
                    activity_action = Action.POSTED
                elif self.status == Tweet.SCHEDULED:
                    activity_action = Action.SCHEDULED
                else:
                    activity_action = Action.CREATED

                self.created = current_datetime

        self.last_modified = current_datetime
        super(Tweet, self).save(*args, **kwargs)

        # Save an action for this update
        action = Action(action=activity_action,
            tweet=self)
        action.save()

        # Send a redis message that a tweet has changed
        self.send_updates(activity_action)

        # If the action was anything except edited, update all clients'
        # badge counts asynchronously
        if activity_action != Action.EDITED:
            publish_counts.apply_async(args=[self.handle.organization.id])

    @classmethod
    def get_pending_count(cls, org_id):
        return cls.objects.filter(handle__organization__id=org_id, status=Tweet.PENDING).count()

    @classmethod
    def get_scheduled_count(cls, org_id):
        return cls.objects.filter(handle__organization__id=org_id, status=Tweet.SCHEDULED).count()

    @classmethod
    def get_counts(cls, org_id):
        counts = {}

        counts['pending'] = cls.get_pending_count(org_id)
        counts['scheduled'] = cls.get_scheduled_count(org_id)

        return counts

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

    def send_updates(self, action):
        if action == Action.CREATED:
            message = 'new'
            send_push_notifications.apply_async(args=[self.body, self.handle.organization.id, self.last_editor.id])
        else:
            message = self.id

        r.publish(self.handle.organization.id, message)

@receiver(post_save, sender=Tweet)
def update_scheduling(sender, instance, **kwargs):
    # If this tweet has a tweet_id, it has already been published
    if instance.twitter_id or instance.status != Tweet.SCHEDULED:
        return

    # Check if the ETA hasn't been updated since this tweet was last saved
    eta_not_updated = getattr(instance, 'eta_not_updated', False)

    # If the ETA wasn't updated, don't schedule another, redundant, task
    if not eta_not_updated:
        publish_later.apply_async(args=[instance.id], eta=instance.eta)

@receiver(post_save, sender=Tweet)
def set_eta_check(sender, instance, **kwargs):
    if instance.status == Tweet.PENDING and instance.eta:
        check_eta.apply_async(args=[instance.id], eta=instance.eta)
