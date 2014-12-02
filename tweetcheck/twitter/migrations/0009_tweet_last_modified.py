# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0008_auto_20141129_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 1, 18, 42, 56, 621594), auto_now=True),
            preserve_default=False,
        ),
    ]
