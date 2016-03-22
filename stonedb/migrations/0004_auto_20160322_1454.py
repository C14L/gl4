# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0003_auto_20151231_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='classification',
            field=models.ForeignKey(blank=True, related_name='stones', to='stonedb.Classification', null=True, default=None, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='stone',
            name='color',
            field=models.ForeignKey(blank=True, related_name='stones', to='stonedb.Color', null=True, default=None, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='stone',
            name='country',
            field=models.ForeignKey(blank=True, related_name='stones', to='stonedb.Country', null=True, default=None, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='stone',
            name='texture',
            field=models.ForeignKey(blank=True, related_name='stones', to='stonedb.Texture', null=True, default=None, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
