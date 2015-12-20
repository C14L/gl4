# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
                ('simple_name', models.CharField(max_length=100, default='')),
                ('simple_slug', models.SlugField(max_length=100, default='')),
            ],
            options={
                'verbose_name': 'classification',
                'verbose_name_plural': 'classifications',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'color',
                'verbose_name_plural': 'colors',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
                ('cc', models.CharField(max_length=1, default='')),
            ],
            options={
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Stone',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, editable=False, default='')),
                ('urlname', models.CharField(max_length=100, editable=False, default='', db_index=True)),
                ('created', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(editable=False, default=django.utils.timezone.now)),
                ('picfile', models.CharField(max_length=100, default='')),
                ('city_name', models.CharField(max_length=50)),
                ('lat', models.FloatField(null=True, default=None)),
                ('lng', models.FloatField(null=True, default=None)),
                ('color_name', models.CharField(max_length=100, default='')),
                ('country_name', models.CharField(max_length=100, default='')),
                ('classification_name', models.CharField(max_length=100, default='')),
                ('texture_name', models.CharField(max_length=100, default='')),
                ('application', models.TextField(default='')),
                ('availability', models.TextField(default='')),
                ('comment', models.TextField(default='')),
                ('maxsize', models.TextField(default='')),
                ('maxsize_block_w', models.PositiveIntegerField(default=0)),
                ('maxsize_block_h', models.PositiveIntegerField(default=0)),
                ('maxsize_block_d', models.PositiveIntegerField(default=0)),
                ('maxsize_slab_w', models.PositiveIntegerField(default=0)),
                ('maxsize_slab_h', models.PositiveIntegerField(default=0)),
                ('hardness', models.FloatField(null=True, default=None)),
                ('uv_resistance', models.FloatField(null=True, default=None)),
                ('classification', models.ForeignKey(null=True, related_name='stones', default=None, to='stonedb.Classification', blank=True)),
                ('color', models.ForeignKey(null=True, related_name='stones', default=None, to='stonedb.Color', blank=True)),
                ('country', models.ForeignKey(null=True, related_name='stones', default=None, to='stonedb.Country', blank=True)),
                ('secondary_colors', models.ManyToManyField(to='stonedb.Color')),
            ],
            options={
                'verbose_name': 'stone',
                'verbose_name_plural': 'stones',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StoneName',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, default='')),
                ('stone', models.ForeignKey(to='stonedb.Stone', related_name='pseu')),
            ],
            options={
                'verbose_name': 'stone name',
                'verbose_name_plural': 'stone names',
            },
        ),
        migrations.CreateModel(
            name='Texture',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'texture',
                'verbose_name_plural': 'textures',
                'ordering': ('slug',),
            },
        ),
        migrations.AddField(
            model_name='stone',
            name='texture',
            field=models.ForeignKey(null=True, related_name='stones', default=None, to='stonedb.Texture', blank=True),
        ),
        migrations.AlterIndexTogether(
            name='stone',
            index_together=set([('lat', 'lng'), ('color', 'classification', 'country')]),
        ),
    ]
