# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20141028_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='img',
            field=models.ImageField(null=True, upload_to='announce/'),
        ),
    ]
