# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('username', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='OfficialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('official_account', models.OneToOneField(primary_key=True, serialize=False, to='database.OfficialAccount')),
                ('user_submit', models.CharField(max_length=32)),
                ('operator_admin', models.CharField(max_length=32)),
                ('status', models.CharField(max_length=10)),
                ('manager_name', models.CharField(max_length=30)),
                ('manager_dept', models.CharField(max_length=40)),
                ('manager_tel', models.CharField(max_length=20)),
                ('manager_email', models.CharField(max_length=254)),
            ],
        ),
    ]
