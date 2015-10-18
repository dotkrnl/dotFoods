# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wikipage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageKeyword',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('keyword', models.CharField(max_length=128)),
                ('count', models.IntegerField()),
                ('page', models.ForeignKey(to='wikipage.WikiPage')),
            ],
        ),
    ]
