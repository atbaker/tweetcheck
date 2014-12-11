# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import twitter.models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0014_auto_20141204_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='eta',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tweet',
            name='body',
            field=models.CharField(validators=[twitter.models.validate_tweet_body], max_length=250),
        ),
    ]
