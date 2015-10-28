# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='admin',
            field=models.ForeignKey(to='database.Admin', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 31, 42, 856573, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
