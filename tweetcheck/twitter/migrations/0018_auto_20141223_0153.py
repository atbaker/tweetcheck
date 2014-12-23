# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0017_remove_tweet_task_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='last_modified',
            field=models.DateTimeField(),
        ),
    ]
