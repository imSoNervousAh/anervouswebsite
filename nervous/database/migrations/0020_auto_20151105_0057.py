# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_accountrecord_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='dept',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='tel',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
