# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20151015_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='avatar_url',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
