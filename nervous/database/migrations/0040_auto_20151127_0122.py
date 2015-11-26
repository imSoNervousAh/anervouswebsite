# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0039_application_reject_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forewarnrule',
            name='account',
            field=models.ForeignKey(blank=True, to='database.OfficialAccount', null=True),
        ),
        migrations.AlterField(
            model_name='forewarnrule',
            name='notification',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='\u9884\u8b66\u65f6\u9650\u81f3\u5c11\u4e3a1\u5929'), django.core.validators.MaxValueValidator(365, message='\u9884\u8b66\u65f6\u9650\u81f3\u591a\u4e3a365\u5929')]),
        ),
    ]
