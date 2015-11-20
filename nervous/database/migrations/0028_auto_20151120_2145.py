# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0027_auto_20151120_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '\u5b66\u751f', 'verbose_name_plural': '\u5b66\u751f'},
        ),
        migrations.RemoveField(
            model_name='message',
            name='title',
        ),
    ]
