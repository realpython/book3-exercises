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
            model_name='user',
            name='bigCoID',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
