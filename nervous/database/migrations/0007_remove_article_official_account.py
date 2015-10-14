# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_application_manager_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='official_account',
        ),
    ]
