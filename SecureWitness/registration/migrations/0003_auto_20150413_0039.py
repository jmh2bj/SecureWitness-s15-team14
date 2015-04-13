# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150413_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='allowed_groups',
            field=models.ManyToManyField(verbose_name='Allowed Groups', null=True, blank=True, to='auth.Group'),
            preserve_default=True,
        ),
    ]
