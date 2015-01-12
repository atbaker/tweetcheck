# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141203_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('token', models.CharField(max_length=64)),
                ('arn', models.CharField(blank=True, max_length=150)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='action',
            name='action',
            field=models.IntegerField(choices=[(-1, 'rejected'), (0, 'created'), (1, 'posted'), (2, 'edited'), (3, 'scheduled')]),
        ),
    ]
