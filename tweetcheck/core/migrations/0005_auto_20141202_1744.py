# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_action'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='action',
            name='body',
            field=models.CharField(max_length=250, default='placeholder string'),
            preserve_default=False,
        ),
    ]
