# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('text', models.TextField(blank=True, default='')),
                ('simple_name', models.CharField(blank=True, default='', max_length=100)),
                ('simple_slug', models.SlugField(blank=True, default='', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'classifications',
                'verbose_name': 'classification',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('text', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name_plural': 'colors',
                'verbose_name': 'color',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('text', models.TextField(blank=True, default='')),
                ('cc', models.CharField(default='xx', max_length=2)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'verbose_name': 'country',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Stone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(default='', editable=False, max_length=100)),
                ('urlname', models.CharField(db_index=True, default='', editable=False, max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('picfile', models.CharField(blank=True, default='', max_length=100)),
                ('city_name', models.CharField(blank=True, max_length=50)),
                ('lat', models.FloatField(blank=True, default=None, null=True)),
                ('lng', models.FloatField(blank=True, default=None, null=True)),
                ('color_name', models.CharField(blank=True, default='', editable=False, max_length=100)),
                ('country_name', models.CharField(blank=True, default='', editable=False, max_length=100)),
                ('classification_name', models.CharField(blank=True, default='', editable=False, max_length=100)),
                ('texture_name', models.CharField(blank=True, default='', editable=False, max_length=100)),
                ('application', models.TextField(blank=True, default='')),
                ('availability', models.TextField(blank=True, default='')),
                ('comment', models.TextField(blank=True, default='')),
                ('maxsize', models.TextField(blank=True, default='')),
                ('maxsize_block_w', models.PositiveIntegerField(blank=True, default=0)),
                ('maxsize_block_h', models.PositiveIntegerField(blank=True, default=0)),
                ('maxsize_block_d', models.PositiveIntegerField(blank=True, default=0)),
                ('maxsize_slab_w', models.PositiveIntegerField(blank=True, default=0)),
                ('maxsize_slab_h', models.PositiveIntegerField(blank=True, default=0)),
                ('hardness', models.FloatField(blank=True, default=None, null=True)),
                ('uv_resistance', models.FloatField(blank=True, default=None, null=True)),
                ('classification', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stones', to='stonedb.Classification')),
                ('color', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stones', to='stonedb.Color')),
                ('country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stones', to='stonedb.Country')),
                ('secondary_colors', models.ManyToManyField(blank=True, to='stonedb.Color')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'stone',
                'verbose_name_plural': 'stones',
            },
        ),
        migrations.CreateModel(
            name='StoneName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('stone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pseu', to='stonedb.Stone')),
            ],
            options={
                'verbose_name_plural': 'stone names',
                'verbose_name': 'stone name',
            },
        ),
        migrations.CreateModel(
            name='Texture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(default='', max_length=100)),
                ('text', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name_plural': 'textures',
                'verbose_name': 'texture',
                'ordering': ('slug',),
            },
        ),
        migrations.AddField(
            model_name='stone',
            name='texture',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stones', to='stonedb.Texture'),
        ),
        migrations.AlterIndexTogether(
            name='stone',
            index_together=set([('color', 'classification', 'country'), ('lat', 'lng')]),
        ),
    ]
