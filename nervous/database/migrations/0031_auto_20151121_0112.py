# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0030_auto_20151121_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='tel',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(regex=b'^\\d{3,12}$', message=b'\xe8\xaf\xb7\xe8\xbe\x93\xe5\x85\xa5\xe4\xb8\x80\xe4\xb8\xaa\xe5\x90\x88\xe6\xb3\x95\xe7\x9a\x84\xe7\x94\xb5\xe8\xaf\x9d\xe5\x8f\xb7\xe7\xa0\x81')]),
        ),
    ]
