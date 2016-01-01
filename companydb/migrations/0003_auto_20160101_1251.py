# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0002_auto_20151231_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
