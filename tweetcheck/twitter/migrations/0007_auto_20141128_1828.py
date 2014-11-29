# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0006_auto_20141128_1825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='handle',
            old_name='twitter_id',
            new_name='user_id',
        ),
    ]
