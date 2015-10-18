# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WikiCategory',
            fields=[
                ('url_name', models.CharField(primary_key=True, serialize=False, max_length=128)),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='WikiList',
            fields=[
                ('url_name', models.CharField(primary_key=True, serialize=False, max_length=128)),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='WikiPage',
            fields=[
                ('url_name', models.CharField(primary_key=True, serialize=False, max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('body', models.TextField(null=True)),
                ('origin', models.URLField(null=True)),
                ('categories', models.ManyToManyField(to='wikipage.WikiCategory')),
                ('lists', models.ManyToManyField(to='wikipage.WikiList')),
            ],
        ),
    ]
