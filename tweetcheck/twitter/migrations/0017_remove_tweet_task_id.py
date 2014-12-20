# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0016_auto_20141219_1750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='task_id',
        ),
    ]
