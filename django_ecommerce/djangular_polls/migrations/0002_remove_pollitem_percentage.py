# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangular_polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollitem',
            name='percentage',
        ),
    ]
