# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0016_auto_20151028_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='posttime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 4, 10, 3, 40, 681490, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
