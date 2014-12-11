# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20141120_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketingitem',
            name='button_link',
            field=models.CharField(blank=True, max_length=200, null=True, default='register'),
        ),
        migrations.AlterField(
            model_name='marketingitem',
            name='img',
            field=models.ImageField(upload_to='marketing/'),
        ),
    ]
