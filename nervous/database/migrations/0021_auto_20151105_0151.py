# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_auto_20151105_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialaccount',
            name='wx_id',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
