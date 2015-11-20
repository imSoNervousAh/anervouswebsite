# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0026_auto_20151120_0324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='officialaccount',
            options={'verbose_name': '\u5fae\u4fe1\u516c\u4f17\u53f7', 'verbose_name_plural': '\u5fae\u4fe1\u516c\u4f17\u53f7'},
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='description',
            field=models.CharField(max_length=300, verbose_name='\u516c\u4f17\u53f7\u7b80\u4ecb'),
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='wx_id',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u516c\u4f17\u53f7\u5fae\u4fe1ID'),
        ),
    ]
