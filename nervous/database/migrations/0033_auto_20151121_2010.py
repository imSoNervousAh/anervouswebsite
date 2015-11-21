# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0032_auto_20151121_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='admin',
            field=models.ForeignKey(blank=True, to='database.Admin', null=True),
        ),
    ]
