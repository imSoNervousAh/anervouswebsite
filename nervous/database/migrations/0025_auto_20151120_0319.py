# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0024_forewarnrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialaccount',
            name='description',
            field=models.CharField(max_length=300, verbose_name='\u516c\u4f17\u53f7\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='name',
            field=models.CharField(max_length=40, verbose_name='\u516c\u4f17\u53f7\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='wx_id',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u516c\u4f17\u53f7ID'),
        ),
    ]
