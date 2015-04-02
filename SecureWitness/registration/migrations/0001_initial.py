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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rep_title', models.CharField(max_length=200)),
                ('rep_created', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('short_desc', models.CharField(max_length=200)),
                ('detailed_desc', models.CharField(max_length=2000)),
                ('rep_date', models.DateTimeField(verbose_name='report date')),
                ('keywords', models.CharField(max_length=500)),
                ('file', models.FileField(blank=True, upload_to='reports')),
                ('isPublic', models.BooleanField(default=True)),
                ('allowed_groups', models.ManyToManyField(to='auth.Group')),
                ('allowed_users', models.ManyToManyField(related_name='allowed_users', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(unique=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
