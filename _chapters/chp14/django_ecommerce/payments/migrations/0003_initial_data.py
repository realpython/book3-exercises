# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations
from payments.models import User


def create_default_user(apps, schema_editor):
    try:
        vader = User.objects.get(email="darth@mec.com")
        vader.delete()
    except User.DoesNotExist:
        pass

    new_user = User.create(
        name='vader', email="darth@mec.com",
        password="darkside", last_4_digits="1234"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_user)
    ]
