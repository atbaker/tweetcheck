# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_handle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='handle',
            options={'ordering': ('screen_name',)},
        ),
        migrations.RenameField(
            model_name='handle',
            old_name='name',
            new_name='screen_name',
        ),
    ]
