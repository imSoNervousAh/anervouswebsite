# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0023_admin_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForewarnRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('target', models.IntegerField()),
                ('value', models.IntegerField()),
                ('account', models.ForeignKey(to='database.OfficialAccount')),
            ],
        ),
    ]
