# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('urlname', models.SlugField(max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('picfile', models.CharField(max_length=100, default='')),
                ('country_name', models.CharField(max_length=100)),
                ('city_name', models.CharField(max_length=50)),
                ('country', models.PositiveIntegerField()),
                ('lat', models.FloatField(default=None, null=True)),
                ('lng', models.FloatField(default=None, null=True)),
                ('color', models.PositiveIntegerField(default=None, null=True)),
                ('secondary_colors', models.CommaSeparatedIntegerField(max_length=250, default=None, null=True)),
                ('classification', models.PositiveIntegerField(default=None, null=True)),
                ('texture', models.PositiveIntegerField(default=None, null=True)),
                ('simpletype', models.CharField(max_length=50, default=None, null=True)),
                ('application', models.TextField(default='')),
                ('availability', models.TextField(default='')),
                ('comment', models.TextField(default='')),
                ('maxsize', models.TextField(default='')),
                ('maxsize_block_w', models.PositiveIntegerField(default=0)),
                ('maxsize_block_h', models.PositiveIntegerField(default=0)),
                ('maxsize_block_d', models.PositiveIntegerField(default=0)),
                ('maxsize_slab_w', models.PositiveIntegerField(default=0)),
                ('maxsize_slab_h', models.PositiveIntegerField(default=0)),
                ('hardness', models.FloatField(default=None, null=True)),
                ('uv_resistance', models.FloatField(default=None, null=True)),
            ],
            options={
                'verbose_name': 'Stone',
                'verbose_name_plural': 'Stones',
            },
        ),
        migrations.CreateModel(
            name='StoneName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('urlname', models.SlugField(max_length=100)),
                ('stone', models.ForeignKey(to='stonedb.Stone', related_name='pseu')),
            ],
            options={
                'verbose_name': 'StoneName',
                'verbose_name_plural': 'StoneNames',
            },
        ),
        migrations.AlterIndexTogether(
            name='stone',
            index_together=set([('lat', 'lng'), ('color', 'classification', 'country')]),
        ),
    ]
