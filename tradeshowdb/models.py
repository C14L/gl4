# from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Tradeshow(models.Model):
    aumaid = models.PositiveIntegerField(db_index=True, default=0)
    name = models.CharField(max_length=60, default='')
    aka = models.CharField(max_length=255, default='')
    url = models.SlugField(max_length=60, db_index=True, default='')
    city_name = models.CharField(max_length=60, default='')
    country_name = models.CharField(max_length=60, default='')
    # country = models.ForeignKey(Countries)  --> TODO: country names table.
    begins = models.DateField(null=True, default=None)
    ends = models.DateField(null=True, default=None)
    keywords = models.TextField(default='')
    about = models.TextField(default='')
    web = models.CharField(max_length=250, default='')
    contact = models.CharField(max_length=250, default='')
    logo = models.CharField(max_length=60, default='')
    # fotos = models.ForeignKey(Fotos)  --> TODO: global fotos table.
    ip = models.CharField(max_length=15, default='')
    time = models.DateTimeField(default=now)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'tradeshow'
        verbose_name_plural = 'tradeshows'
        ordering = ('begins', )

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return self.url

    @slug.setter
    def slug(self, val):
        self.url = val
