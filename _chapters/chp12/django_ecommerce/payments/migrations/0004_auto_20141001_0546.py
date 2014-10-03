# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bigCoID',
            field=models.CharField(max_length=50,
                                   default=datetime.datetime.now(), unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unpaidusers',
            name='last_notification',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 1, 5, 44, 20, 437687)),
        ),
    ]
