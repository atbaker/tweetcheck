# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetcheckuser',
            name='organization',
            field=models.ForeignKey(blank=True, to='core.Organization', null=True),
        ),
    ]
