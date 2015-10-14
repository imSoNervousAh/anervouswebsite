# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_application_association'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='manager_student_id',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
