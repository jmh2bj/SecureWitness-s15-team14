# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('rep_title', models.CharField(max_length=200)),
                ('rep_created', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('short_desc', models.CharField(max_length=200)),
                ('detailed_desc', models.CharField(max_length=2000)),
                ('rep_date', models.DateTimeField(verbose_name='report date')),
                ('keywords', models.CharField(max_length=500)),
                ('file', models.FileField(blank=True, null=True, upload_to='reports')),
                ('isPublic', models.BooleanField(default=True)),
                ('allowed_groups', models.ManyToManyField(null=True, to='auth.Group')),
                ('allowed_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, related_name='allowed_users')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
