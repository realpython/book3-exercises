# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        ('payments', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(to='payments.User', to_field='id')),
                ('when', models.DateTimeField(blank=True)),
                ('status', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
