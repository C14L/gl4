# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0008_auto_20151030_2023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stone',
            options={'verbose_name_plural': 'Stones', 'ordering': ['name'], 'verbose_name': 'Stone'},
        ),
        migrations.RemoveField(
            model_name='stone',
            name='country_name',
        ),
        migrations.AlterField(
            model_name='stone',
            name='country',
            field=models.PositiveIntegerField(default=None, null=True, choices=[(0, 'czech republic'), (0, 'great britain'), (0, 'saudi arabia'), (0, 'south africa'), (0, 'sri lanka'), (24, 'angola'), (32, 'argentina'), (36, 'australia'), (40, 'austria'), (51, 'armenia'), (56, 'belgium'), (68, 'bolivia'), (76, 'brazil'), (100, 'bulgaria'), (124, 'canada'), (156, 'china'), (158, 'china'), (191, 'croatia'), (192, 'cuba'), (210, 'ethiopia'), (246, 'finland'), (250, 'france'), (268, 'georgia'), (276, 'germany'), (300, 'greece'), (320, 'guatemala'), (356, 'india'), (364, 'iran'), (372, 'ireland'), (376, 'israel'), (380, 'italy'), (392, 'japan'), (398, 'kasahstan'), (450, 'madagascar'), (458, 'malaysia'), (484, 'mexico'), (496, 'mongolia'), (504, 'morocco'), (508, 'mozambique'), (516, 'namibia'), (566, 'nigeria'), (578, 'norway'), (586, 'pakistan'), (604, 'peru'), (616, 'poland'), (620, 'portugal'), (643, 'russia'), (682, 'saudi arabia'), (704, 'vietnam'), (705, 'slovenia'), (710, 'south africa'), (716, 'zimbabwe'), (724, 'spain'), (736, 'sudan'), (752, 'sweden'), (756, 'switzerland'), (792, 'turkey'), (788, 'tunisia'), (804, 'ukraine'), (807, 'macedonia'), (818, 'egypt'), (840, 'usa'), (858, 'uruguay'), (862, 'venezuela'), (891, 'yugoslavia'), (894, 'zambia')]),
        ),
        migrations.AlterField(
            model_name='stone',
            name='created',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='stone',
            name='simpletype',
            field=models.CharField(editable=False, default=None, null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='stone',
            name='slug',
            field=models.SlugField(editable=False, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='stone',
            name='updated',
            field=models.DateTimeField(editable=False, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='stone',
            name='urlname',
            field=models.CharField(editable=False, default='', db_index=True, max_length=100),
        ),
    ]
