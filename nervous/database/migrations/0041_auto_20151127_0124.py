# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0040_auto_20151127_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forewarnrule',
            name='duration',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='\u9884\u8b66\u65f6\u9650\u81f3\u5c11\u4e3a1\u5929'), django.core.validators.MaxValueValidator(365, message='\u9884\u8b66\u65f6\u9650\u81f3\u591a\u4e3a365\u5929')]),
        ),
        migrations.AlterField(
            model_name='forewarnrule',
            name='notification',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='forewarnrule',
            name='value',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='\u8be5\u503c\u5e94\u4e3a\u6b63\u6570')]),
        ),
    ]
