from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Classification(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', db_index=True)
    text = models.TextField(default='')
    simple_name = models.CharField(max_length=100, default='')
    simple_slug = models.SlugField(max_length=100, default='', db_index=True)


class Color(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', db_index=True)
    text = models.TextField(default='')


class Country(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', db_index=True)
    cc = models.CharField(max_length=1, default='')
    text = models.TextField(default='')


class Texture(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', db_index=True)
    text = models.TextField(default='')


class Stone(models.Model):
    CLASSIFICATION_CHOICES = [
        (x[0], x[1]) for x in getattr(settings, 'CLASSIFICATION_DATA', ())]
    COLOR_CHOICES = [
        (x[0], x[1]) for x in getattr(settings, 'COLOR_DATA', ())]
    TEXTURE_CHOICES = [
        (x[0], x[1]) for x in getattr(settings, 'TEXTURE_DATA', ())]
    COUNTRY_CHOICES = [
        (x[0], x[1]) for x in getattr(settings, 'COUNTRY_DATA', ())]
    SIMPLETYPE_CHOICES = getattr(settings, 'SIMPLETYPE_CHOICES', ())

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

    def _get_data_field(self, k, v, data):
        try:
            return [x[k] for x in data if x[0] == v][0]
        except IndexError:
            return ''

    def get_color_slug(self):
        return self._get_data_field(1, self.color, settings.COLOR_DATA)

    def get_color_name(self):
        return self._get_data_field(2, self.color, settings.COLOR_DATA)

    def get_country_slug(self):
        return self._get_data_field(1, self.country, settings.COUNTRY_DATA)

    def get_country_name(self):
        return self._get_data_field(2, self.country, settings.COUNTRY_DATA)

    def get_country_cc(self):
        return self._get_data_field(3, self.country, settings.COUNTRY_DATA)

    def get_classification_slug(self):
        return self._get_data_field(1, self.classification,
                                    settings.CLASSIFICATION_DATA)

    def get_classification_name(self):
        return self._get_data_field(2, self.classification,
                                    settings.CLASSIFICATION_DATA)

    def get_texture_slug(self):
        return self._get_data_field(1, self.texture, settings.TEXTURE_DATA)

    def get_texture_name(self):
        return self._get_data_field(2, self.texture, settings.TEXTURE_DATA)

    def get_pic_fname_default(self):
        """Return standard file name for pictures."""
        return '{}.jpg'.format(self.slug)

    def get_pic_fname(self):
        """Return custom picfile or the standard file name."""
        if self.picfile:
            return self.picfile
        else:
            return self.get_pic_fname_default()

    def get_pic_thumb(self):
        """Return complete URL for thumb size pic."""
        return '/stonesindex/{}'.format(self.get_pic_fname())

    def get_pic_medium(self):
        """Return complete URL for medium size pic."""
        return '/stonespics/{}'.format(self.get_pic_fname())

    def get_pic_large(self):
        """Return complete URL for large size pic (don't exist yet)."""
        return '/granite-photos/{}'.format(self.get_pic_fname())

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
