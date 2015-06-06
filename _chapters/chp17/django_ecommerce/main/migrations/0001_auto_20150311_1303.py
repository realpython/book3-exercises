# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', 'data_load_marketing_items_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='img',
            field=models.ImageField(null=True, blank=True, upload_to='announce/'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='vid',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='img',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
