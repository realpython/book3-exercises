# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_bigcoid(apps, schema_editor):

    User = apps.get_model('payments', 'User')

    for u in User.objects.all():
        bid = ("%s%s%s" % (u.name[:2],
                            u.rank[:1],
                            u.created_at.strftime("%Y%m%d%H%M%S%f"),
                          ))

        u.bigCoID = bid
        u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20141001_0546'),
    ]

    operations = [
        migrations.RunPython(migrate_bigcoid)
    ]
