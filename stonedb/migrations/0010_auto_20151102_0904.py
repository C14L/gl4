# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stonedb', '0009_auto_20151101_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='stone',
            name='classification_name',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='stone',
            name='color_name',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='stone',
            name='country_name',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='stone',
            name='texture_name',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='stone',
            name='classification',
            field=models.PositiveIntegerField(null=True, choices=[(0, 'amazonite - granite'), (0, 'foidolite'), (0, 'hornblende-amphibolite'), (0, 'iron ore'), (0, 'marble-onyx'), (0, 'mikrolin-quatrz -phyllite'), (0, 'n/a'), (0, 'n.a'), (0, 'orbicular granite'), (0, 'orthoklase - quartz - phyllite'), (0, 'quartz -phyllite'), (0, 'phyllite'), (0, 'sodalite-syenite'), (0, 'schist'), (0, 'serizite-quatrz-phyllite'), (0, 'sodalithe-gneiss'), (0, 'sodalithe-syenite'), (2, 'anhydrite'), (3, 'anorthosite'), (4, 'aplite'), (5, 'basalt'), (6, 'charnockite'), (8, 'cordierite'), (9, 'diabase'), (10, 'diorite'), (13, 'gabbro'), (14, 'gneiss'), (15, 'granite'), (17, 'granodiorite'), (18, 'granulite'), (19, 'hornfels'), (20, 'limestone'), (21, 'conglomerate'), (22, 'lamprophyre'), (23, 'lava'), (25, 'marble'), (26, 'metatexite'), (27, 'migmatite'), (30, 'monzonite'), (32, 'norite'), (33, 'ophicalcite'), (35, 'orthogneiss'), (37, 'paragneiss'), (38, 'pegmatite'), (39, 'porphyry'), (41, 'quartzite'), (42, 'rhyolite'), (43, 'sandstone'), (44, 'slate'), (46, 'serpentinite'), (48, 'soapstone'), (50, 'spessartite'), (51, 'syenite'), (52, 'tonalite'), (53, 'trachyte'), (54, 'travertine'), (55, 'tuff')], default=None),
        ),
        migrations.AlterField(
            model_name='stone',
            name='country',
            field=models.PositiveIntegerField(null=True, choices=[(24, 'angola'), (32, 'argentina'), (36, 'australia'), (40, 'austria'), (51, 'armenia'), (56, 'belgiumBelgium'), (68, 'bolivia'), (76, 'brazil'), (100, 'bulgaria'), (124, 'canada'), (156, 'china'), (158, 'china'), (191, 'croatia'), (192, 'cuba'), (210, 'ethiopia'), (246, 'finland'), (250, 'france'), (268, 'georgia'), (276, 'germany'), (300, 'greece'), (320, 'guatemala'), (356, 'india'), (364, 'iran'), (372, 'ireland'), (376, 'israel'), (380, 'italy'), (392, 'japan'), (398, 'kasakhstan'), (450, 'madagascar'), (458, 'malaysia'), (484, 'mexico'), (496, 'mongolia'), (504, 'morocco'), (508, 'mozambique'), (516, 'namibia'), (566, 'nigeria'), (578, 'norway'), (586, 'pakistan'), (604, 'peru'), (616, 'poland'), (620, 'portugal'), (643, 'russia'), (682, 'saudi-arabia'), (704, 'vietnam'), (705, 'slovenia'), (710, 'south-africa'), (716, 'zimbabwe'), (724, 'spain'), (736, 'sudan'), (752, 'sweden'), (756, 'switzerland'), (792, 'turkey'), (788, 'tunisia'), (804, 'ukraine'), (807, 'macedonia'), (818, 'egypt'), (840, 'usa'), (858, 'uruguay'), (862, 'venezuela'), (891, 'yugoslavia'), (894, 'zambia')], default=None),
        ),
    ]
