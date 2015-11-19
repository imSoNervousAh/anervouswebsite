# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0025_auto_20151120_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='operator_admin',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
