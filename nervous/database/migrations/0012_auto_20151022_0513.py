# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_article_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleDailyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('update_time', models.DateTimeField()),
                ('likes', models.IntegerField()),
                ('views', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='article',
            name='views',
        ),
        migrations.AddField(
            model_name='articledailyrecord',
            name='article',
            field=models.ForeignKey(to='database.Article'),
        ),
    ]
