# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0008_auto_20141129_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='last_modified',
            field=models.DateTimeField(default=timezone.now(), auto_now=True),
            preserve_default=False,
        ),
    ]
