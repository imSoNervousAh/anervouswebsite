# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0049_auto_20151128_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='forewarnrule',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 22, 7, 16, 591620, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
