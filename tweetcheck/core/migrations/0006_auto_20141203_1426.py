# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141202_1744'),
    ]

    operations = [
    migrations.RemoveField(
            model_name='action',
            name='action',
        ),
        migrations.AddField(
            model_name='action',
            name='action',
            field=models.IntegerField(choices=[(-1, 'rejected'), (0, 'created'), (1, 'posted'), (2, 'edited')]),
        ),
    ]
