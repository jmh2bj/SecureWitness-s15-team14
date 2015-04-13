# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='contained_folders',
            field=models.ManyToManyField(null=True, to='registration.Folder'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(max_length=200, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='rep_title',
            field=models.CharField(max_length=200, unique=True),
            preserve_default=True,
        ),
    ]
