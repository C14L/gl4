# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tradeshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aumaid', models.PositiveIntegerField(default=0, db_index=True)),
                ('name', models.CharField(default='', max_length=60)),
                ('aka', models.CharField(default='', max_length=255)),
                ('url', models.SlugField(default='', max_length=60)),
                ('city_name', models.CharField(default='', max_length=60)),
                ('country_name', models.CharField(default='', max_length=60)),
                ('begins', models.DateField(default=None, null=True)),
                ('ends', models.DateField(default=None, null=True)),
                ('keywords', models.TextField(default='')),
                ('about', models.TextField(default='')),
                ('web', models.CharField(default='', max_length=250)),
                ('contact', models.CharField(default='', max_length=250)),
                ('logo', models.CharField(default='', max_length=60)),
                ('ip', models.CharField(default='', max_length=15)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_edited', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
            ],
        ),
    ]
