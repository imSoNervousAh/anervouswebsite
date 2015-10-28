# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_auto_20151028_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(serialize=False, primary_key=True)),
                ('real_name', models.CharField(max_length=20)),
            ],
        ),
    ]
