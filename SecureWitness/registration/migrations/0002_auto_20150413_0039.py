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
            name='detailed_desc',
            field=models.CharField(verbose_name='Detailed Description', max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='isPublic',
            field=models.BooleanField(verbose_name='Public Report?', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.CharField(verbose_name='Associated Keywords', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_date',
            field=models.DateTimeField(verbose_name='Report date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='short_desc',
            field=models.CharField(verbose_name='Short Description', max_length=200),
            preserve_default=True,
        ),
    ]
