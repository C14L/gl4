# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0003_auto_20160101_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pic',
            options={'verbose_name_plural': 'Pictures', 'verbose_name': 'Picture', 'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='pic',
            name='caption',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='pic',
            name='title',
            field=models.CharField(default='', blank=True, max_length=80),
        ),
    ]
