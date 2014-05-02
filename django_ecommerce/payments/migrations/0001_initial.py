# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('main', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnpaidUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('last_notification', models.DateTimeField(default=datetime.datetime(2014, 5, 1, 21, 43, 50, 465957))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(unique=True, max_length=255)),
                ('rank', models.CharField(default='Padwan', max_length=50)),
                ('last_4_digits', models.CharField(null=True, blank=True, max_length=4)),
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
