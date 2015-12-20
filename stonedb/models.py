from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.timezone import now


class CommonStonePropertyManager(models.Manager):
    def all_with_stones(self):
        """
        Return a list of all items that are a property of at least one stone.
        Each object as "stones__count" with the number of stones it is a
        property of.
        """
        return self.all().annotate(Count('stones'))\
            .filter(stones__count__gte=1).exclude(name__exact='')


class CommonStoneProperty(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', db_index=True)
    text = models.TextField(default='')

    objects = CommonStonePropertyManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Classification(CommonStoneProperty):
    simple_name = models.CharField(max_length=100, default='')
    simple_slug = models.SlugField(max_length=100, default='', db_index=True)

    class Meta:
        verbose_name = "classification"
        verbose_name_plural = "classifications"
        ordering = ('slug', )


class Color(CommonStoneProperty):

    class Meta:
        verbose_name = "color"
        verbose_name_plural = "colors"
        ordering = ('slug', )


class Country(CommonStoneProperty):
    cc = models.CharField(max_length=2, default='xx')

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"
        ordering = ('slug', )


class Texture(CommonStoneProperty):

    class Meta:
        verbose_name = "texture"
        verbose_name_plural = "textures"
        ordering = ('slug', )


class Stone(models.Model):
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

    country = models.ForeignKey(Country, blank=True, null=True, default=None,
                                related_name='stones')
    texture = models.ForeignKey(Texture, blank=True, null=True, default=None,
                                related_name='stones')
    classification = models.ForeignKey(Classification, blank=True, null=True,
                                       default=None, related_name='stones')
    color = models.ForeignKey(Color, blank=True, null=True, default=None,
                              related_name='stones')
    secondary_colors = models.ManyToManyField(Color)

    # + + +  not used, just for import verification  + + +
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
        verbose_name = "stone"
        verbose_name_plural = "stones"
        index_together = [['lat', 'lng'],
                          ['color', 'classification', 'country'], ]
        ordering = ['name']

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
        verbose_name = "stone name"
        verbose_name_plural = "stone names"

    def __str__(self):
        return self.name
