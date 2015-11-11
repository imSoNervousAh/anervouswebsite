# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0021_auto_20151105_0151'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForewarnRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('duration', models.IntegerField()),
                ('notification', models.IntegerField()),
                ('target', models.IntegerField()),
                ('value', models.IntegerField()),
                ('account', models.ForeignKey(to='database.OfficialAccount', null=True)),
            ],
        ),
    ]
