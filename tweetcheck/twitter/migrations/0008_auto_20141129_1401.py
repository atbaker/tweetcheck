# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0007_auto_20141128_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handle',
            name='user_id',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]
