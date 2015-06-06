# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_auto_20150311_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='vid',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='marketingitem',
            name='button_link',
            field=models.CharField(default='register', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='marketingitem',
            name='img',
            field=models.ImageField(upload_to='marketing/'),
        ),
    ]
