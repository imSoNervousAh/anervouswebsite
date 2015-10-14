# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_remove_article_official_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='official_account_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
