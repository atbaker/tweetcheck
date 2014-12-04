# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0013_tweet_twitter_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='twitter_id',
        ),
        migrations.AddField(
            model_name='tweet',
            name='twitter_id',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
