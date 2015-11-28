# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0050_forewarnrule_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'verbose_name': '\u7ba1\u7406\u5458', 'verbose_name_plural': '\u7ba1\u7406\u5458'},
        ),
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=20, serialize=False, verbose_name='\u8be5\u7528\u6237\u540d', primary_key=True),
        ),
    ]
