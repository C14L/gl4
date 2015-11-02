from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Stone(models.Model):
    CLASSIFICATION_CHOICES = getattr(settings, 'CLASSIFICATION_CHOICES', ())
    COLOR_CHOICES = getattr(settings, 'COLOR_CHOICES', ())
    COUNTRY_CHOICES = getattr(settings, 'COUNTRY_CHOICES', ())
    SIMPLETYPE_CHOICES = getattr(settings, 'SIMPLETYPE_CHOICES', ())
    TEXTURE_CHOICES = getattr(settings, 'TEXTURE_CHOICES', ())

    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='',
                            db_index=True, editable=False)
    urlname = models.CharField(max_length=100, db_index=True,  # OLD 'urlname',
                               default='', editable=False)     # for redir only
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(default=now, editable=False)  # update_time

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

    # TODO: lookup lat/lng for city/location names
    city_name = models.CharField(max_length=50)
    lat = models.FloatField(null=True, default=None)
    lng = models.FloatField(null=True, default=None)

    color = models.PositiveIntegerField(
        choices=COLOR_CHOICES, null=True, default=None)
    secondary_colors = models.CommaSeparatedIntegerField(
        choices=COLOR_CHOICES, null=True, default=None, max_length=250)
    classification = models.PositiveIntegerField(
        choices=CLASSIFICATION_CHOICES, null=True, default=None)
    country = models.PositiveIntegerField(
        choices=COUNTRY_CHOICES, null=True, default=None)
    texture = models.PositiveIntegerField(
        choices=TEXTURE_CHOICES, null=True, default=None)
    simpletype = models.CharField(
        choices=SIMPLETYPE_CHOICES, null=True, default=None, max_length=50,
        editable=False)

    # not used, just for import verification
    color_name = models.CharField(max_length=100, default='')
    country_name = models.CharField(max_length=100, default='')
    classification_name = models.CharField(max_length=100, default='')
    texture_name = models.CharField(max_length=100, default='')

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
        ordering = ['name']

    def get_pic_fname(self):
        """Return picfile or the standard file name for all main pictures."""
        if self.picfile:
            return self.picfile
        return '{}-{}-{}.jpg'.format(self.slug, self.get_color_display,
                                     self.get_classification_display)

    def get_pic_thumb(self):
        return '/stonesindex/{}'.format(self.get_pic_fname)

    def get_pic_medium(self):
        return '/stonespics/{}'.format(self.get_pic_fname)

    def get_pseudonyms(self):
        return ', '.join([x.name for x in self.pseu.all()])

    def __str__(self):
        return self.name


class StoneName(models.Model):
    stone = models.ForeignKey(Stone, related_name='pseu')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default='', db_index=True)

    class Meta:
        verbose_name = "StoneName"
        verbose_name_plural = "StoneNames"

    def __str__(self):
        return self.name
