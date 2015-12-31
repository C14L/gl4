# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0002_auto_20151220_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='simple_name',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='classification',
            name='simple_slug',
            field=models.SlugField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='classification',
            name='text',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='text',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='text',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='application',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='availability',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='city_name',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='classification_name',
            field=models.CharField(default='', max_length=100, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='color_name',
            field=models.CharField(default='', max_length=100, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='comment',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='country_name',
            field=models.CharField(default='', max_length=100, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='hardness',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='lat',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='lng',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='maxsize',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='maxsize_block_d',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='maxsize_block_h',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='maxsize_block_w',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='maxsize_slab_h',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='maxsize_slab_w',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='picfile',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='secondary_colors',
            field=models.ManyToManyField(to='stonedb.Color', blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='texture_name',
            field=models.CharField(default='', max_length=100, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='uv_resistance',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='texture',
            name='text',
            field=models.TextField(default='', blank=True),
        ),
    ]
