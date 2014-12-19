# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0015_auto_20141211_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='task_id',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tweet',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, 'pending'), (1, 'posted'), (-1, 'rejected'), (3, 'scheduled')]),
        ),
    ]
