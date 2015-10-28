# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0002_auto_20151028_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='stone',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='stone',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='stone',
            name='urlname',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
    ]
