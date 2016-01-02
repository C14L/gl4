# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdpages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name_plural': 'Articles', 'verbose_name': 'Article', 'ordering': ('-created',)},
        ),
    ]