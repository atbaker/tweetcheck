from django.conf import settings
from django.db import models
from requests_oauthlib import OAuth1

import requests

class Tweet(models.Model):
    body = models.CharField(max_length=250)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u'{0}'.format(self.body)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Tweet.objects.get(pk=self.pk)
            if (not original.approved) and self.approved:
                self.publish()
        super(Tweet, self).save(*args, **kwargs)

    def publish(self):
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        auth = OAuth1(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET,
                  settings.ATB_ACCESS_TOKEN, settings.ATB_TOKEN_SECRET)
        payload = {
            'status': self.body,
        }

        # TO-DO: Add some error handling here
        requests.post(url, auth=auth, params=payload)
        return
