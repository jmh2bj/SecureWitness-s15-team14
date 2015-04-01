# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('rep_title', models.CharField(max_length=200)),
                ('rep_created', models.DateTimeField(verbose_name='date created')),
                ('short_desc', models.CharField(max_length=200)),
                ('detailed_desc', models.CharField(max_length=2000)),
                ('loc', models.CharField(max_length=200)),
                ('rep_date', models.DateTimeField(verbose_name='report date')),
                ('keywords', models.CharField(max_length=500)),
                ('file', models.FileField(upload_to='reports', blank=True)),
                ('isPublic', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'permissions': [('admin', 'Is a SecureWitness Admin')],
            },
            bases=(models.Model,),
        ),
    ]
