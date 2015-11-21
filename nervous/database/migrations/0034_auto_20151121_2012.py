# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0033_auto_20151121_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='admin',
            field=models.ForeignKey(to='database.Admin', null=True),
        ),
    ]
