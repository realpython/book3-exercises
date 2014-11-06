# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangular_polls', '0002_remove_pollitem_percentage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pollitem',
            options={'ordering': ['-text']},
        ),
        migrations.AlterField(
            model_name='pollitem',
            name='poll',
            field=models.ForeignKey(related_name='items', to='djangular_polls.Poll'),
        ),
    ]
