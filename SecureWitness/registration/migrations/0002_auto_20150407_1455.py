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
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='allowed_users', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
