# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companydb', '0003_auto_20151106_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastlogin_ip',
            field=models.CharField(max_length=15, default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='signup_ip',
            field=models.CharField(max_length=15, default=''),
        ),
    ]
