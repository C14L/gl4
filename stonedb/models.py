import json

from os.path import join

from django.conf import settings
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify as dj_slugify
from django.utils.timezone import now


STONE_PROPERTIES = None


def slugify(s):
    """Fix Django's slugify with some transliterations before slugifying."""
    tr = {'ü': 'ue', 'Ü': 'ue', 'ö': 'oe', 'Ö': 'Oe', 'ä': 'ae', 'Ä': 'Ae',
          'ß': 'ss', '_': '-', }

    for k, v in tr.items():
        s = s.replace(k, v)

    return dj_slugify(s)


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
    slug = models.SlugField(max_length=100, default='')
    text = models.TextField(default='', blank=True)

    objects = CommonStonePropertyManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Classification(CommonStoneProperty):
    simple_name = models.CharField(max_length=100, default='', blank=True)
    simple_slug = models.SlugField(max_length=100, default='', db_index=True,
                                   blank=True)

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

    @property
    def flag_path(self):
        return join(settings.STATIC_URL, 'img/flags', self.cc + '.png')


class Texture(CommonStoneProperty):

    class Meta:
        verbose_name = "texture"
        verbose_name_plural = "textures"
        ordering = ('slug', )


class Stone(models.Model):
    name = models.CharField(max_length=100, default='', db_index=True)
    slug = models.SlugField(max_length=100, default='', editable=False)
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
    picfile = models.CharField(max_length=100, default='', blank=True)

    # TODO: additional pics all frmo media
    # title_foto = models.ForeignKey(Fotos, null=True, default=None)
    # is_use_title_foto = models.BooleanField(default=False)

    # TODO: lookup lat/lng for city/location names
    city_name = models.CharField(max_length=50, blank=True)
    lat = models.FloatField(null=True, default=None, blank=True)
    lng = models.FloatField(null=True, default=None, blank=True)

    country = models.ForeignKey(Country, models.SET_NULL,
                                related_name='stones', db_index=True,
                                blank=True, null=True, default=None)
    texture = models.ForeignKey(Texture, models.SET_NULL,
                                related_name='stones', db_index=True,
                                blank=True, null=True, default=None)
    classification = models.ForeignKey(Classification, models.SET_NULL,
                                       related_name='stones', db_index=True,
                                       blank=True, null=True, default=None)
    color = models.ForeignKey(Color, models.SET_NULL,
                              related_name='stones', db_index=True,
                              blank=True, null=True, default=None)
    secondary_colors = models.ManyToManyField(Color, blank=True)

    # + + +  not used, just for import verification  + + +
    color_name = models.CharField(max_length=100, default='',
                                  editable=False, blank=True)
    country_name = models.CharField(max_length=100, default='',
                                    editable=False, blank=True)
    classification_name = models.CharField(max_length=100, default='',
                                           editable=False, blank=True)
    texture_name = models.CharField(max_length=100, default='',
                                    editable=False, blank=True)

    application = models.TextField(default='', blank=True)
    availability = models.TextField(default='', blank=True)
    comment = models.TextField(default='', blank=True)

    maxsize = models.TextField(default='', blank=True)
    maxsize_block_w = models.PositiveIntegerField(default=0, blank=True)
    maxsize_block_h = models.PositiveIntegerField(default=0, blank=True)
    maxsize_block_d = models.PositiveIntegerField(default=0, blank=True)
    maxsize_slab_w = models.PositiveIntegerField(default=0, blank=True)
    maxsize_slab_h = models.PositiveIntegerField(default=0, blank=True)

    # TODO: add more technical data.
    hardness = models.FloatField(null=True, default=None, blank=True)
    uv_resistance = models.FloatField(null=True, default=None, blank=True)

    class Meta:
        verbose_name = "stone"
        verbose_name_plural = "stones"
        index_together = [['lat', 'lng'],
                          ['color', 'classification', 'country'], ]
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_admin_url(self):
        return reverse('admin:{}_{}_change'.format(
            self._meta.app_label, self._meta.model_name), args=[self.id])

    def get_absolute_url(self):
        return reverse('stonedb_item', args=[self.slug])

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


class StoneName(models.Model):
    stone = models.ForeignKey(
            Stone, on_delete=models.SET_NULL, null=True, related_name='pseu')
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, default='')

    class Meta:
        verbose_name = "stone name"
        verbose_name_plural = "stone names"

    def __str__(self):
        return self.name


@receiver(post_save, sender=Classification)
@receiver(post_save, sender=Color)
@receiver(post_save, sender=Country)
@receiver(post_save, sender=Texture)
@receiver(post_delete, sender=Classification)
@receiver(post_delete, sender=Color)
@receiver(post_delete, sender=Country)
@receiver(post_delete, sender=Texture)
def _updated_stone_property(sender, **kwargs):
    """
    If any searchable property is changed, rebuild properties.
    """
    get_stone_properties(refresh=True)


def get_stone_properties(refresh=False):
    global STONE_PROPERTIES

    if not STONE_PROPERTIES or refresh:
        STONE_PROPERTIES = {
            m.__name__.lower(): list(m.objects.all_with_stones().values('id', 'slug', 'name'))
            for m in (Classification, Color, Country, Texture)
        }
    return STONE_PROPERTIES
