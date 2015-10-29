# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0006_auto_20151029_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
