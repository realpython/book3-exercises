# encoding: utf8
from django.db import models, migrations
import datetime
import django.utils.timezone
from payments.models import User

def create_default_user(apps, schema_editor):
    existingUsers = apps.get_model("payments","User")
    vader = existingUsers.objects.filter(email="darth@mec.com")
    if vader: vader[0].delete()
    new_user = User.create(name='vader', email="darth@mec.com",
                        password="darkside",last_4_digits="1234")



class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_user)
    ]
