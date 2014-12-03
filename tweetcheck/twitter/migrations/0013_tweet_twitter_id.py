# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0012_auto_20141203_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='twitter_id',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
