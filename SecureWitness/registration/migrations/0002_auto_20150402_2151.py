# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='allowed_groups',
            field=models.ManyToManyField(to='auth.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='allowed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='allowed_users', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='file',
            field=models.FileField(upload_to='reports', null=True, blank=True),
            preserve_default=True,
        ),
    ]
