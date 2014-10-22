from django.db import models

class Tweet(models.Model):
    body = models.CharField(max_length=250)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u'{0}'.format(self.body)
