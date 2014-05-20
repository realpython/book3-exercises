# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('publish_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('poll', models.ForeignKey(to_field='id', to='djangular_polls.Poll')),
                ('name', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=300)),
                ('votes', models.IntegerField(default=0)),
                ('percentage', models.Field(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
