from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Stone(models.Model):
    COLOR_CH = getattr(settings, 'COLOR_CHOICES', ())
    TEXTURE_CH = getattr(settings, 'TEXTURE_CHOICES', ())
    CLASSIF_CH = getattr(settings, 'CLASSIFICATION_CHOICES', ())
    SIMPLETYPE_CH = getattr(settings, 'SIMPLETYPE_CHOICES', ())

    name = models.CharField(max_length=100)
    urlname = models.SlugField(max_length=100, db_index=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)  # --> update_time

    # TODO: use "StoneName"."pseu"
    # pseudonym = models.TextField(default='')

    # TODO: main pic automatically from pics or spics dirs with pic filename
    # auto generated from stone name, color, classification. Unless the picture
    # filename is manually set here.
    # smallpic = models.CharField(max_length=100, default='')
    # largepic = models.CharField(max_length=100, default='')
    # projectpic = models.CharField(max_length=100, default='')
    picfile = models.CharField(max_length=100, default='')

    # TODO: additional pics all frmo media
    # title_foto = models.ForeignKey(Fotos, null=True, default=None)
    # is_use_title_foto = models.BooleanField(default=False)

    # TODO: country --> country_name, and city --> city_name
    # but also use cities geo database to lookup proximity to larger cities.
    country_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=50)
    country = models.PositiveIntegerField()
    # country = models.ForeignKey(Country, null=True, default=None)
    lat = models.FloatField(null=True, default=None)
    lng = models.FloatField(null=True, default=None)

    # TODO:
    # color_id --> color
    # texture_id --> texture
    # classification_id --> classification
    # type_url --> simpletype
    color = models.PositiveIntegerField(
        choices=COLOR_CH, null=True, default=None)
    secondary_colors = models.CommaSeparatedIntegerField(
        choices=COLOR_CH, null=True, default=None)
    classification = models.PositiveIntegerField(
        choices=CLASSIF_CH, null=True, default=None)
    texture = models.PositiveIntegerField(
        choices=TEXTURE_CH, null=True, default=None)
    simpletype = models.CharField(
        choices=SIMPLETYPE_CH, null=True, default=None)

    application = models.TextField(default='')
    availability = models.TextField(default='')
    comment = models.TextField(default='')

    maxsize = models.TextField(default='')
    maxsize_block_w = models.PositiveIntegerField(default=0)
    maxsize_block_h = models.PositiveIntegerField(default=0)
    maxsize_block_d = models.PositiveIntegerField(default=0)
    maxsize_slab_w = models.PositiveIntegerField(default=0)
    maxsize_slab_h = models.PositiveIntegerField(default=0)

    # TODO: add more technical data.
    hardness = models.FloatField(null=True, default=None)
    uv_resistance = models.FloatField(null=True, default=None)

    class Meta:
        verbose_name = "Stone"
        verbose_name_plural = "Stones"
        index_together = [['lat', 'lng'],
                          ['color', 'classification', 'country'], ]

    def __str__(self):
        self.name


class StoneName(models.Model):
    stone = models.ForeignKey(Stone, related_name='pseu')
    name = models.CharField(max_length=100)
    urlname = models.SlugField(max_length=100, db_index=True)

    class Meta:
        verbose_name = "StoneName"
        verbose_name_plural = "StoneNames"

    def __str__(self):
        self.name
