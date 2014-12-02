# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitter', '0009_tweet_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='author',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tweet',
            name='last_editor',
            field=models.ForeignKey(related_name='+', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
