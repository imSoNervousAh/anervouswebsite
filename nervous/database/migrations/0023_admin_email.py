# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0022_forewarnrule'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='email',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
    ]
