# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0029_auto_20151121_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=254, validators=[django.core.validators.EmailValidator(message=b'\xe8\xaf\xb7\xe8\xbe\x93\xe5\x85\xa5\xe4\xb8\x80\xe4\xb8\xaa\xe5\x90\x88\xe6\xb3\x95\xe7\x9a\x84\xe9\x82\xae\xe4\xbb\xb6\xe5\x9c\xb0\xe5\x9d\x80')]),
        ),
    ]
