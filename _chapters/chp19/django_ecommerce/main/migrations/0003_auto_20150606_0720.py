# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150311_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusreport',
            name='when',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
