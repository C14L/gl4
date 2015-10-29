# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0005_auto_20151028_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='slug',
            field=models.SlugField(max_length=100, default=''),
        ),
    ]
