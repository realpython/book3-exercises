# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_bigcoId_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unpaidusers',
            name='last_notification',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 7, 9, 4, 17, 68581)),
        ),
        migrations.AlterField(
            model_name='user',
            name='bigCoID',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
