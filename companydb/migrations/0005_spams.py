# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-26 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0004_auto_20160412_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spams',
            fields=[
                ('match', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]