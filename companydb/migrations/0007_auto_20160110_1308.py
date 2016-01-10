# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0006_auto_20160107_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='description',
            field=models.TextField(default='', verbose_name='Stock items description', blank=True, help_text='Please add any information about the stock items here, i.e. sizes, surface treatment, borders, etc.'),
        ),
    ]
