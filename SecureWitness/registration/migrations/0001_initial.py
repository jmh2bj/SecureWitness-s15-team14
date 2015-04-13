# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rep_title', models.CharField(max_length=200, verbose_name='Report Title')),
                ('rep_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('short_desc', models.CharField(max_length=200)),
                ('detailed_desc', models.CharField(max_length=2000)),
                ('rep_date', models.DateTimeField(verbose_name='report date')),
                ('keywords', models.CharField(max_length=500)),
                ('isPublic', models.BooleanField(default=True)),
                ('allowed_groups', models.ManyToManyField(null=True, to='auth.Group', blank=True)),
                ('allowed_users', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, related_name='allowed_users', blank=True)),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rep_file', models.FileField(null=True, upload_to='reports', blank=True)),
                ('isEncrypted', models.BooleanField(default=False)),
                ('report', models.ForeignKey(to='registration.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
