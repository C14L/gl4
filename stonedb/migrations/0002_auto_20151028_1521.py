# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='country',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
