# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0011_auto_20151106_0020'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('slug', models.CharField(max_length=30)),
                ('about', models.TextField(default='')),
                ('description', models.CharField(max_length=255, default='')),
                ('keywords', models.CharField(max_length=255, default='')),
                ('count_members', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Groups',
                'verbose_name': 'Group',
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('group', models.ForeignKey(to='companydb.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('module', models.CharField(choices=[('profile', 'Profile'), ('fotos', 'Photos'), ('stock', 'Stock'), ('forum', 'Forum'), ('pages', 'Pages')], max_length=20)),
                ('module_id', models.PositiveIntegerField(default=0)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('size', models.PositiveIntegerField()),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('ext', models.CharField(max_length=3, default='jpg')),
                ('title', models.CharField(max_length=80, default='')),
                ('caption', models.TextField()),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_sticky', models.BooleanField(default=False)),
                ('is_comments', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_title', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pictures',
                'verbose_name': 'Picture',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_recommended', models.BooleanField(default=False)),
                ('count_views', models.PositiveIntegerField(default=0)),
                ('stone', models.ForeignKey(to='stonedb.Stone')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stocks',
                'verbose_name': 'Stock',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_recommended', models.BooleanField(default=False)),
                ('count_views', models.PositiveIntegerField(default=0)),
                ('stone', models.ForeignKey(to='stonedb.Stone')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Stocks',
                'verbose_name': 'Stock',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('contact', models.CharField(max_length=100, default='')),
                ('contact_position', models.CharField(max_length=100, default='')),
                ('slogan', models.CharField(max_length=255, default='')),
                ('street', models.CharField(max_length=100, default='')),
                ('city', models.CharField(max_length=100, default='')),
                ('zip', models.CharField(max_length=16, default='')),
                ('country_sub_id', models.PositiveIntegerField(db_index=True)),
                ('country_id', models.PositiveIntegerField(db_index=True)),
                ('country_sub_name', models.CharField(max_length=100, default='')),
                ('country_name', models.CharField(max_length=100, default='')),
                ('postal', models.TextField(default='')),
                ('email', models.CharField(max_length=100, default='')),
                ('fax', models.CharField(max_length=100, default='')),
                ('tel', models.CharField(max_length=100, default='')),
                ('mobile', models.CharField(max_length=100, default='')),
                ('web', models.CharField(max_length=100, default='')),
                ('about', models.TextField(default='')),
                ('title_foto', models.IntegerField()),
                ('title_foto_ext', models.CharField(max_length=30, default='')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='title_foto',
            field=models.ForeignKey(to='companydb.Pic'),
        ),
    ]
