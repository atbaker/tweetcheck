# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_auto_20141201_1848'),
        ('core', '0003_auto_20141107_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=2, choices=[(b'CR', b'created'), (b'ED', b'edited'), (b'PO', b'posted')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='core.Organization')),
                ('tweet', models.ForeignKey(to='twitter.Tweet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
