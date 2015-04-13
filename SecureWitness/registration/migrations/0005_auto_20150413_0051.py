# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20150413_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportfile',
            name='report',
        ),
        migrations.DeleteModel(
            name='ReportFile',
        ),
        migrations.AddField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to='reports', null=True, blank=True),
            preserve_default=True,
        ),
    ]
