# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MarketingItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('heading', models.CharField(max_length=300)),
                ('caption', models.TextField()),
                ('button_link', models.URLField(default='register', null=True)),
                ('button_title', models.CharField(max_length=20, default='View details')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now=True)),
                ('img', models.CharField(max_length=255, null=True)),
                ('vid', models.URLField(null=True)),
                ('info', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
