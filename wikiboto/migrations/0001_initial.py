# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotoFinished',
            fields=[
                ('url', models.CharField(primary_key=True, serialize=False, max_length=128)),
            ],
        ),
    ]
