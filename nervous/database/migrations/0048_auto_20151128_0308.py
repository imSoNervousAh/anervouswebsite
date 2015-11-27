# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0047_auto_20151128_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrecord',
            name='articles_acc',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountrecord',
            name='wci',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
