from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Stone(models.Model):
    COLOR_CH = getattr(settings, 'COLOR_CHOICES', ())
    TEXTURE_CH = getattr(settings, 'TEXTURE_CHOICES', ())
    CLASSIF_CH = getattr(settings, 'CLASSIFICATION_CHOICES', ())

    name = models.CharField(max_length=100)
    urlname = models.SlugField(max_length=100)
    # pseudonym = models.TextField(default='') --> use "StoneName"."pseu"

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

    country_name = models.CharField(max_length=63)
    # country = models.ForeignKey(Country)
    city_name = models.CharField(max_length=50)

    color = models.PositiveIntegerField(choices=COLOR_CH)  # --> color_id
    classification = models.PositiveIntegerField(choices=CLASSIF_CH)
    # --> classification_id
    texture = models.PositiveIntegerField(choices=TEXTURE_CH)  # --> texture_id

    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)  # --> update_time

    application = models.TextField(default='')
    availability = models.TextField(default='')
    comment = models.TextField(default='')

    maxsize = models.TextField(default='')
    maxsize_block_w = models.PositiveIntegerField(default=0)
    maxsize_block_h = models.PositiveIntegerField(default=0)
    maxsize_block_d = models.PositiveIntegerField(default=0)
    maxsize_slab_w = models.PositiveIntegerField(default=0)
    maxsize_slab_h = models.PositiveIntegerField(default=0)

    type_url = models.CharField(max_length=20, default='')

    class Meta:
        verbose_name = "Stone"
        verbose_name_plural = "Stones"

    def __str__(self):
        self.name


class StoneName(models.Model):
    stone = models.ForeignKey(Stone, related_name='pseu')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "StoneName"
        verbose_name_plural = "StoneNames"

    def __str__(self):
        self.name
