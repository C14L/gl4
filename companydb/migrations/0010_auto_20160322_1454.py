# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0009_auto_20160321_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='slogan',
            field=models.CharField(blank=True, verbose_name='Company slogan', max_length=255, help_text='A very short sentence that expresses the company focus and values.', default=''),
        ),
    ]
