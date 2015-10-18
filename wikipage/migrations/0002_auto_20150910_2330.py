# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wikipage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikicategory',
            name='url_name',
            field=models.CharField(serialize=False, primary_key=True, max_length=128, db_index=True),
        ),
        migrations.AlterField(
            model_name='wikilist',
            name='url_name',
            field=models.CharField(serialize=False, primary_key=True, max_length=128, db_index=True),
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='categories',
            field=models.ManyToManyField(to='wikipage.WikiCategory', db_index=True),
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='lists',
            field=models.ManyToManyField(to='wikipage.WikiList', db_index=True),
        ),
        migrations.AlterField(
            model_name='wikipage',
            name='url_name',
            field=models.CharField(serialize=False, primary_key=True, max_length=128, db_index=True),
        ),
    ]
