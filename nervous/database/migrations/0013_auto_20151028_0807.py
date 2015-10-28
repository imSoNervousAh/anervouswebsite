# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20151022_0513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articledailyrecord',
            name='article',
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.CharField(unique=True, max_length=300),
        ),
        migrations.DeleteModel(
            name='ArticleDailyRecord',
        ),
    ]
