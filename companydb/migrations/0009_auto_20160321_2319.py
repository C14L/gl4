# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0008_auto_20160120_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title_foto',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='stock',
            name='dim_total',
            field=models.PositiveIntegerField(help_text='Total amount in square meters or cubic meters.', default=0, blank=True, verbose_name='Total amount'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='slogan',
            field=models.CharField(help_text='A very short sentence thath expresses the company focus and values.', default='', blank=True, max_length=255, verbose_name='Company slogan'),
        ),
    ]
