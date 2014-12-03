# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141203_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='tweet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='twitter.Tweet'),
        ),
    ]
