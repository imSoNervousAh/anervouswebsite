# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0037_auto_20151124_0213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Globals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('announcement', models.CharField(default=b'', max_length=256)),
            ],
        ),
    ]
