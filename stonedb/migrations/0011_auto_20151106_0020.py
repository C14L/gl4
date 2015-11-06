# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0010_auto_20151102_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
                ('simple_name', models.CharField(max_length=100, default='')),
                ('simple_slug', models.SlugField(max_length=100, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('cc', models.CharField(max_length=1, default='')),
                ('text', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Texture',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, default='')),
                ('slug', models.SlugField(max_length=100, default='')),
                ('text', models.TextField(default='')),
            ],
        ),
        migrations.AlterField(
            model_name='stone',
            name='texture',
            field=models.PositiveIntegerField(null=True, choices=[(0, 'coarse-grained'), (0, 'coarse-grained'), (0, 'coarse-grained'), (0, 'coarse-grained'), (0, 'coarse-grained'), (0, 'veined-coarse-grained'), (0, 'fine-grained'), (0, 'fine-grained'), (0, 'fine-grained'), (0, 'fine-grained'), (0, 'veined-fine-grained'), (0, 'fine-grained'), (0, 'medium-grained'), (0, 'fine-grained'), (0, 'medium-grained'), (0, 'veined-fine-grained'), (0, 'veined'), (0, 'coarse-grained'), (0, 'medium-grained'), (0, 'medium-grained'), (0, 'medium-grained'), (0, 'medium-grained'), (0, 'medium-grained'), (0, 'dunno'), (0, 'veined'), (0, 'veined')], default=None),
        ),
    ]
