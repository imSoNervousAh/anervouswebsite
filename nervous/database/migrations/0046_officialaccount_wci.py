# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0045_auto_20151128_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialaccount',
            name='wci',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
