# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0018_accountrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrecord',
            name='account',
            field=models.ForeignKey(default=None, to='database.OfficialAccount'),
            preserve_default=False,
        ),
    ]
