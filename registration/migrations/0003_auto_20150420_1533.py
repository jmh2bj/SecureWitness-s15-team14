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
            field=models.CharField(verbose_name='Associated Keywords', null=True, blank=True, max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='loc',
            field=models.CharField(verbose_name='Location', null=True, blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
