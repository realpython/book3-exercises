# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20141120_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='img',
            field=models.ImageField(blank=True, upload_to='announce/', null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='vid',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
