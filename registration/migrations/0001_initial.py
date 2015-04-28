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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('rep_title', models.CharField(max_length=200, verbose_name='Report Title')),
                ('rep_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('short_desc', models.CharField(max_length=200, verbose_name='Short Description')),
                ('detailed_desc', models.CharField(max_length=2000, verbose_name='Detailed Description')),
                ('loc', models.CharField(max_length=200, blank=True, null=True, verbose_name='Location')),
                ('rep_date', models.DateTimeField(blank=True, null=True, verbose_name='Report date')),
                ('keywords', models.CharField(max_length=500, blank=True, null=True, verbose_name='Associated Keywords')),
                ('rep_file', models.FileField(upload_to='reports', blank=True, null=True)),
                ('isPublic', models.BooleanField(default=True, verbose_name='Public Report?')),
                ('views', models.IntegerField(default=0)),
                ('allowed_groups', models.ManyToManyField(blank=True, null=True, verbose_name='Allowed Groups', to='auth.Group')),
                ('allowed_users', models.ManyToManyField(blank=True, related_name='allowed_users', null=True, verbose_name='Allowed Users', to=settings.AUTH_USER_MODEL)),
                ('downvotes', models.ManyToManyField(blank=True, related_name='downvotes', null=True, verbose_name='Users who have downvoted this report', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
                ('upvotes', models.ManyToManyField(blank=True, related_name='upvotes', null=True, verbose_name='Users who have upvoted this report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
            options={
                'permissions': [('admin', 'Is a SecureWitness Admin')],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='folder',
            name='contained_reports',
            field=models.ManyToManyField(blank=True, null=True, to='registration.Report'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
