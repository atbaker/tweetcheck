# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0005_handle_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='handle',
            name='name',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='handle',
            name='profile_image_url',
            field=models.URLField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='handle',
            name='twitter_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
