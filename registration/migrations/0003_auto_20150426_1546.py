# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150420_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.CharField(verbose_name='Associated Keywords', max_length=500, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='loc',
            field=models.CharField(verbose_name='Location', max_length=200, blank=True, null=True),
            preserve_default=True,
        ),
    ]
