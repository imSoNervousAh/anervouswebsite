# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0042_auto_20151127_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialaccount',
            name='likes_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='officialaccount',
            name='views_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='officialaccount',
            name='wci',
            field=models.FloatField(null=True),
        ),
    ]
