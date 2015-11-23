# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0035_officialaccount_update_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialaccount',
            name='update_status',
            field=models.IntegerField(default=0, choices=[(0, b'normal'), (1, b'pending_update'), (2, b'updating'), (3, b'pending_check'), (4, b'finished')]),
        ),
    ]
