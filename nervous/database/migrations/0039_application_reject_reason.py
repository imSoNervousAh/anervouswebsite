# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0038_globals'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='reject_reason',
            field=models.CharField(max_length=140, blank=True),
        ),
    ]
