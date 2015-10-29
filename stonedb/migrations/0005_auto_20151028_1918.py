# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0004_auto_20151028_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stone',
            name='classification',
            field=models.PositiveIntegerField(null=True, default=None, choices=[(0, 'amazonite - granite'), (0, 'foidolite'), (0, 'hornblende-amphibolite'), (0, 'iron ore'), (0, 'marble-onyx'), (0, 'mikrolin-quatrz -phyllite'), (0, 'n/a'), (0, 'n.a'), (0, 'orbicular granite'), (0, 'orthoklase - quartz - phyllite'), (0, 'quartz -phyllite'), (0, 'phyllite'), (0, 'sodalite-syenite'), (0, 'schist'), (0, 'serizite-quatrz-phyllite'), (0, 'sodalithe-gneiss'), (0, 'sodalithe-syenite'), (2, 'anhydrite'), (3, 'anorthosite'), (4, 'aplite'), (5, 'basalt'), (6, 'charnockite'), (8, 'cordierite'), (9, 'diabase'), (10, 'diorite'), (13, 'gabbro'), (14, 'gneiss'), (15, 'granite'), (17, 'granodiorite'), (18, 'granulite'), (19, 'hornfels'), (20, 'limestone'), (21, 'conglomerate'), (22, 'lamprophyre'), (23, 'lava'), (25, 'marble'), (27, 'migmatite'), (26, 'metatexite'), (30, 'monzonite'), (32, 'norite'), (33, 'ophicalcite'), (35, 'orthogneiss'), (35, 'granite'), (37, 'paragneiss'), (38, 'pegmatite'), (39, 'porphyry'), (41, 'quartzite'), (42, 'rhyolite'), (43, 'sandstone'), (44, 'slate'), (46, 'serpentinite'), (46, 'marble'), (48, 'soapstone'), (50, 'spessartite'), (51, 'syenite'), (52, 'tonalite'), (53, 'trachyte'), (54, 'travertine'), (55, 'tuff')]),
        ),
        migrations.AlterField(
            model_name='stone',
            name='color',
            field=models.PositiveIntegerField(null=True, default=None, choices=[(1, 'beige'), (2, 'blue'), (3, 'brown'), (4, 'yellow'), (5, 'grey'), (7, 'green'), (8, 'white'), (9, 'pink'), (10, 'red'), (11, 'black'), (12, 'white')]),
        ),
        migrations.AlterField(
            model_name='stone',
            name='secondary_colors',
            field=models.CommaSeparatedIntegerField(max_length=250, default=None, choices=[(1, 'beige'), (2, 'blue'), (3, 'brown'), (4, 'yellow'), (5, 'grey'), (7, 'green'), (8, 'white'), (9, 'pink'), (10, 'red'), (11, 'black'), (12, 'white')], null=True),
        ),
        migrations.AlterField(
            model_name='stone',
            name='texture',
            field=models.PositiveIntegerField(null=True, default=None, choices=[(0, 'coars'), (0, 'coarse'), (0, 'Coarse'), (0, 'coarse grain'), (0, 'coarse grained'), (0, 'coarse grain, veined'), (0, 'fine'), (0, 'Fine'), (0, 'fine grain'), (0, 'fine grained'), (0, 'fine grained, veined'), (0, 'fine grained, with plenty of large fossils'), (0, 'fine to medium'), (0, 'Fine grained'), (0, 'fine, medium'), (0, 'fine, veined'), (0, 'geädert'), (0, 'grob'), (0, 'medium'), (0, 'Medium'), (0, 'medium grain'), (0, 'medium grained'), (0, 'medium - coarse grain'), (0, 'n/a'), (0, 'veined'), (0, 'Veined')]),
        ),
        migrations.AlterField(
            model_name='stonename',
            name='slug',
            field=models.SlugField(max_length=100, default=''),
        ),
    ]
