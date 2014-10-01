# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', primary_key=True,
                    serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=250)),
                ('topic', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField(
                    default=datetime.datetime.now, auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
    ]
