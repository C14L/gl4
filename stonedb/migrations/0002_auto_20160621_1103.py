# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-21 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=100),
        ),
    ]
