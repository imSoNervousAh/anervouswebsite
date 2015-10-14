# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_admin_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='association',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
