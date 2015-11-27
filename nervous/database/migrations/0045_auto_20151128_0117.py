# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0044_auto_20151127_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officialaccount',
            name='wci',
        ),
        migrations.AddField(
            model_name='accountrecord',
            name='wci',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
