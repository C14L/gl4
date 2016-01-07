# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0003_auto_20151231_1550'),
        ('companydb', '0005_auto_20160107_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='stones',
        ),
        migrations.AddField(
            model_name='project',
            name='lat',
            field=models.FloatField(editable=False, default=None, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='lng',
            field=models.FloatField(editable=False, default=None, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='location',
            field=models.TextField(verbose_name='Address', blank=True, default='', help_text='ONLY for publicly accessible buildings, provide a streetaddress of the project, where it can be visited.'),
        ),
        migrations.AddField(
            model_name='stock',
            name='stone',
            field=models.ForeignKey(to='stonedb.Stone', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='count_views',
            field=models.PositiveIntegerField(editable=False, default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(verbose_name='Project description', blank=True, default='', help_text='Describe the project, the challenges you met, the problems you solved, the time it took, etc.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stock',
            name='count_views',
            field=models.PositiveIntegerField(editable=False, default=0),
        ),
        migrations.AlterField(
            model_name='stock',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='stock',
            name='description',
            field=models.TextField(verbose_name='Project description', blank=True, default='', help_text='Describe the project, the challenges you met, the problems you solved, the time it took, etc.'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
