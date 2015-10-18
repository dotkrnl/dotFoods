# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wikiboto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botofinished',
            name='url',
            field=models.CharField(serialize=False, primary_key=True, max_length=128, db_index=True),
        ),
    ]
