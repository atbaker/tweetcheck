# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('twitter', '0004_tweet_handle'),
    ]

    operations = [
        migrations.AddField(
            model_name='handle',
            name='organization',
            field=models.ForeignKey(default=1, to='core.Organization'),
            preserve_default=False,
        ),
    ]
