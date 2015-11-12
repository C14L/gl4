# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='count_members',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=30, default=''),
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.CharField(max_length=30, default=''),
        ),
        migrations.AlterField(
            model_name='group',
            name='title_foto',
            field=models.ForeignKey(to='companydb.Pic', null=True, default=None),
        ),
        migrations.AlterField(
            model_name='pic',
            name='caption',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='pic',
            name='height',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pic',
            name='module',
            field=models.CharField(max_length=20, choices=[('profile', 'Profile'), ('fotos', 'Photos'), ('stock', 'Stock'), ('forum', 'Forum'), ('pages', 'Pages')], default='profile'),
        ),
        migrations.AlterField(
            model_name='pic',
            name='size',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pic',
            name='width',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country_id',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country_sub_id',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title_foto',
            field=models.IntegerField(default=0),
        ),
    ]
