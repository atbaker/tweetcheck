# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_auto_20141024_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='handle',
            field=models.ForeignKey(default=1, to='twitter.Handle'),
            preserve_default=False,
        ),
    ]
