# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_auto_20141201_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='approved',
        ),
        migrations.AddField(
            model_name='tweet',
            name='status',
            field=models.CharField(default='PE', choices=[('PE', 'pending'), ('PO', 'posted'), ('RE', 'rejected')], max_length=2),
            preserve_default=True,
        ),
    ]
