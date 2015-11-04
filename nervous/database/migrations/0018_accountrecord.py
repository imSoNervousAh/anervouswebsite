# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_article_posttime'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('articles', models.IntegerField()),
                ('likes', models.IntegerField()),
                ('views', models.IntegerField()),
            ],
        ),
    ]
