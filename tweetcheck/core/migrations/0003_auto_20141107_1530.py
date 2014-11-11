# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141107_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweetcheckuser',
            old_name='approver',
            new_name='is_approver',
        ),
    ]
