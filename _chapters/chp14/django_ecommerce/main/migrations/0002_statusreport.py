# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '__first__'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusReport',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('when', models.DateTimeField(blank=True)),
                ('status', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to='payments.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
