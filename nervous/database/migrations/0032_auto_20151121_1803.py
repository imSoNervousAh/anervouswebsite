# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0031_auto_20151121_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]
