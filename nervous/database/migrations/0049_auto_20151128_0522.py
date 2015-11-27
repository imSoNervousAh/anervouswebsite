# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0048_auto_20151128_0308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountrecord',
            name='articles_acc',
        ),
        migrations.RemoveField(
            model_name='accountrecord',
            name='likes_acc',
        ),
        migrations.RemoveField(
            model_name='accountrecord',
            name='views_acc',
        ),
    ]
