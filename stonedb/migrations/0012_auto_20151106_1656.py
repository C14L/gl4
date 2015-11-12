# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0011_auto_20151106_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stone',
            name='simpletype',
        ),
        migrations.AlterField(
            model_name='stone',
            name='classification',
            field=models.ForeignKey(related_name='stones', default=None, to='stonedb.Classification', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='color',
            field=models.ForeignKey(related_name='stones', default=None, to='stonedb.Color', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='country',
            field=models.ForeignKey(related_name='stones', default=None, to='stonedb.Country', blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='stone',
            name='secondary_colors',
        ),
        migrations.AddField(
            model_name='stone',
            name='secondary_colors',
            field=models.ManyToManyField(to='stonedb.Color'),
        ),
        migrations.AlterField(
            model_name='stone',
            name='texture',
            field=models.ForeignKey(related_name='stones', default=None, to='stonedb.Texture', blank=True, null=True),
        ),
    ]
