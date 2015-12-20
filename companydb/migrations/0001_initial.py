# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stonedb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=30, default='')),
                ('slug', models.CharField(max_length=30, default='')),
                ('about', models.TextField(default='')),
                ('description', models.CharField(max_length=255, default='')),
                ('keywords', models.CharField(max_length=255, default='')),
                ('count_members', models.PositiveSmallIntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('module', models.CharField(max_length=20, choices=[('profile', 'Profile'), ('fotos', 'Photos'), ('stock', 'Stock'), ('forum', 'Forum'), ('pages', 'Pages')], default='profile')),
                ('module_id', models.PositiveIntegerField(default=0)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('size', models.PositiveIntegerField(default=0)),
                ('width', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
                ('ext', models.CharField(max_length=3, default='jpg')),
                ('title', models.CharField(max_length=80, default='')),
                ('caption', models.TextField(default='')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_sticky', models.BooleanField(default=False)),
                ('is_comments', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_title', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Picture',
                'verbose_name_plural': 'Pictures',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_recommended', models.BooleanField(default=False)),
                ('count_views', models.PositiveIntegerField(default=0)),
                ('stone', models.ForeignKey(to='stonedb.Stone')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_recommended', models.BooleanField(default=False)),
                ('count_views', models.PositiveIntegerField(default=0)),
                ('stone', models.ForeignKey(to='stonedb.Stone')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('name', models.CharField(max_length=100, default='')),
                ('contact', models.CharField(max_length=100, default='')),
                ('contact_position', models.CharField(max_length=100, default='')),
                ('slogan', models.CharField(max_length=255, default='')),
                ('street', models.CharField(max_length=100, default='')),
                ('city', models.CharField(max_length=100, default='')),
                ('zip', models.CharField(max_length=16, default='')),
                ('country_sub_id', models.PositiveIntegerField(default=0, db_index=True)),
                ('country_id', models.PositiveIntegerField(default=0, db_index=True)),
                ('country_sub_name', models.CharField(max_length=100, default='')),
                ('country_name', models.CharField(max_length=100, default='')),
                ('postal', models.TextField(default='')),
                ('email', models.CharField(max_length=100, default='')),
                ('fax', models.CharField(max_length=100, default='')),
                ('tel', models.CharField(max_length=100, default='')),
                ('mobile', models.CharField(max_length=100, default='')),
                ('web', models.CharField(max_length=100, default='')),
                ('about', models.TextField(default='')),
                ('title_foto', models.IntegerField(default=0)),
                ('title_foto_ext', models.CharField(max_length=30, default='')),
                ('signup_ip', models.CharField(max_length=15, default='')),
                ('lastlogin_ip', models.CharField(max_length=15, default='')),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pic',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='title_foto',
            field=models.ForeignKey(null=True, default=None, to='companydb.Pic'),
        ),
    ]
