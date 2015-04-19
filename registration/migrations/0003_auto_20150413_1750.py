# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150413_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='loc',
            field=models.CharField(blank=True, verbose_name='Location', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.CharField(blank=True, verbose_name='Associated Keywords', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_date',
            field=models.DateTimeField(blank=True, verbose_name='Report date'),
            preserve_default=True,
        ),
    ]
