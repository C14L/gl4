# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0003_auto_20151028_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stonename',
            name='urlname',
        ),
        migrations.AddField(
            model_name='stonename',
            name='slug',
            field=models.SlugField(default='', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='stone',
            name='name',
            field=models.CharField(default='', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='stone',
            name='slug',
            field=models.SlugField(default='', unique=True, max_length=100),
        ),
    ]
