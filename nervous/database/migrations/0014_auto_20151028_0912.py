# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_auto_20151028_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.IntegerField()),
                ('title', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=140)),
                ('processed', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='officialaccount',
            name='wx_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='official_account',
            field=models.ForeignKey(to='database.OfficialAccount'),
        ),
    ]
