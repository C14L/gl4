# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups', 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects', 'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='stock',
            options={'verbose_name': 'Stock', 'verbose_name_plural': 'Stocks', 'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='pic',
            name='module',
            field=models.CharField(default='profile', max_length=20, choices=[('profile', 'Profile'), ('projects', 'Projects'), ('stones', 'Stones'), ('stock', 'Stock'), ('groups', 'Groups'), ('pages', 'Pages')]),
        ),
    ]
