# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0041_auto_20151127_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forewarnrule',
            name='value',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='\u8be5\u503c\u5e94\u4e3a\u6b63\u6570'), django.core.validators.MaxValueValidator(2147483647, message='\u8be5\u503c\u5e94\u572832\u4f4d\u6574\u6570\u8303\u56f4\u5185')]),
        ),
    ]
