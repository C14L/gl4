# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companydb', '0002_auto_20151106_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmember',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id',
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='GroupMember',
        ),
    ]
