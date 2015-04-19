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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('contained_folders', models.ManyToManyField(null=True, to='registration.Folder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('rep_title', models.CharField(verbose_name='Report Title', max_length=200)),
                ('rep_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('short_desc', models.CharField(verbose_name='Short Description', max_length=200)),
                ('detailed_desc', models.CharField(verbose_name='Detailed Description', max_length=2000)),
                ('rep_date', models.DateTimeField(verbose_name='Report date')),
                ('keywords', models.CharField(verbose_name='Associated Keywords', max_length=500)),
                ('file', models.FileField(null=True, upload_to='reports', blank=True)),
                ('isPublic', models.BooleanField(verbose_name='Public Report?', default=True)),
                ('allowed_groups', models.ManyToManyField(verbose_name='Allowed Groups', null=True, blank=True, to='auth.Group')),
                ('allowed_users', models.ManyToManyField(related_name='allowed_users', verbose_name='Allowed Users', null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='folder',
            name='contained_reports',
            field=models.ManyToManyField(null=True, blank=True, to='registration.Report'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
