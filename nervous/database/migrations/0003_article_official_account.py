# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20151010_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='official_account',
            field=models.ForeignKey(default='', to='database.OfficialAccount'),
            preserve_default=False,
        ),
    ]
