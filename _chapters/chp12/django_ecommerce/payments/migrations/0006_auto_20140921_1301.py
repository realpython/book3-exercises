# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20140921_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unpaidusers',
            name='last_notification',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 21, 13, 1, 23, 677271)),
        ),
    ]
