# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0011_auto_20141203_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='status',
        ),
        migrations.AddField(
            model_name='tweet',
            name='status',
            field=models.IntegerField(choices=[(0, 'pending'), (1, 'posted'), (-1, 'rejected')], default=0),
        ),
    ]
