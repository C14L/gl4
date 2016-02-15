# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0007_auto_20160110_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='dim_total',
            field=models.PositiveIntegerField(verbose_name='Total amount', default=0, help_text='The total amount of stock for this product', blank=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='dim_type',
            field=models.PositiveSmallIntegerField(help_text='Specify the product type of of your stock item.', verbose_name='Product type', default=0, choices=[(0, 'not specified'), (1, 'blocks'), (2, 'slabs'), (3, 'tiles'), (4, 'cobblestone'), (9, 'other')], blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='stones',
            field=models.ManyToManyField(null=True, verbose_name='Stones used', default=None, help_text='Start typing the name of a stone used in the project, then select the stones from the list. Add all stones used in the project, but not more than ten.', to='stonedb.Stone'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='description',
            field=models.TextField(verbose_name='Stock item description', default='', help_text='Add any information about the stock item here, i.e. sizes, surface treatment, borders, etc.', blank=True),
        ),
    ]
