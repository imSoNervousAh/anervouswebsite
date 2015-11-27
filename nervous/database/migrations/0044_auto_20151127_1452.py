# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0043_auto_20151127_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='official_account',
            field=models.OneToOneField(to='database.OfficialAccount'),
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='likes_total',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='views_total',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='officialaccount',
            name='wci',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
