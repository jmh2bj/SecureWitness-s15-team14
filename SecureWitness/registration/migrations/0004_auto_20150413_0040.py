# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20150413_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='allowed_users', verbose_name='Allowed Users', null=True),
            preserve_default=True,
        ),
    ]
