# encoding: utf8
from django.db import models, migrations
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnpaidUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('last_notification', models.DateTimeField(default=datetime.datetime(2014, 4, 26, 23, 19, 6, 85457))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('rank', models.CharField(default='Padwan', max_length=50)),
                ('last_4_digits', models.CharField(max_length=4, blank=True, null=True)),
                ('stripe_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badges', models.ManyToManyField(to='main.Badge')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
