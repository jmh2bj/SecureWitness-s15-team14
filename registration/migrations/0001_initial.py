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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('rep_title', models.CharField(verbose_name='Report Title', max_length=200)),
                ('rep_created', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('short_desc', models.CharField(verbose_name='Short Description', max_length=200)),
                ('detailed_desc', models.CharField(verbose_name='Detailed Description', max_length=2000)),
                ('loc', models.CharField(verbose_name='Location', blank=True, max_length=200)),
                ('rep_date', models.DateTimeField(verbose_name='Report date', blank=True)),
                ('keywords', models.CharField(verbose_name='Associated Keywords', blank=True, max_length=500)),
                ('rep_file', models.FileField(blank=True, null=True, upload_to='reports')),
                ('isPublic', models.BooleanField(default=True, verbose_name='Public Report?')),
                ('allowed_groups', models.ManyToManyField(verbose_name='Allowed Groups', to='auth.Group', null=True, blank=True)),
                ('allowed_users', models.ManyToManyField(related_name='allowed_users', verbose_name='Allowed Users', to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('admin', 'Is a SecureWitness Admin')],
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
