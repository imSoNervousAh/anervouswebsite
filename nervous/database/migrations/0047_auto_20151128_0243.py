# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0046_officialaccount_wci'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrecord',
            name='likes_acc',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountrecord',
            name='views_acc',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
