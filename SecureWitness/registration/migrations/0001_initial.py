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
            name='Folder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('contained_folders', models.ManyToManyField(to='registration.Folder', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('rep_title', models.CharField(max_length=200, verbose_name='Report Title')),
                ('rep_created', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('short_desc', models.CharField(max_length=200, verbose_name='Short Description')),
                ('detailed_desc', models.CharField(max_length=2000, verbose_name='Detailed Description')),
                ('rep_date', models.DateTimeField(verbose_name='Report date')),
                ('keywords', models.CharField(max_length=500, verbose_name='Associated Keywords')),
                ('file', models.FileField(blank=True, upload_to='reports', null=True)),
                ('isPublic', models.BooleanField(default=True, verbose_name='Public Report?')),
                ('allowed_groups', models.ManyToManyField(blank=True, verbose_name='Allowed Groups', to='auth.Group', null=True)),
                ('allowed_users', models.ManyToManyField(blank=True, verbose_name='Allowed Users', to=settings.AUTH_USER_MODEL, related_name='allowed_users', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='folder',
            name='contained_reports',
            field=models.ManyToManyField(blank=True, to='registration.Report', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
