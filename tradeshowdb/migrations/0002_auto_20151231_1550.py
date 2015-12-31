# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeshowdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tradeshow',
            options={'verbose_name': 'tradeshow', 'verbose_name_plural': 'tradeshows', 'ordering': ('begins',)},
        ),
    ]
