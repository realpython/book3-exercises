# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('poll', models.ForeignKey(to='djangular_polls.Poll', to_field='id')),
                ('name', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=300)),
                ('votes', models.IntegerField(default=0)),
                ('percentage', models.DecimalField(max_digits=5, default=0.0, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
