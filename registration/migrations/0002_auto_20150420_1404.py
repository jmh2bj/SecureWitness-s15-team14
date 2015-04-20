# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='rep_date',
            field=models.DateTimeField(verbose_name='Report date', blank=True, null=True),
            preserve_default=True,
        ),
    ]
