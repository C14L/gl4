# from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Tradeshow(models.Model):
    aumaid = models.PositiveIntegerField(db_index=True)
    name = models.CharField(max_length=60)
    aka = models.CharField(max_length=255)
    url = models.SlugField(max_length=60, db_index=True)
    city_name = models.CharField(max_length=60)
    country_name = models.CharField(max_length=60)
    # country = models.ForeignKey(Countries)  --> TODO: country names table.
    begins = models.DateField()
    ends = models.DateField()
    keywords = models.TextField()
    about = models.TextField()
    web = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    logo = models.CharField(max_length=60)
    # fotos = models.ForeignKey(Fotos)  --> TODO: global fotos table.
    ip = models.CharField(max_length=15)
    time = models.DateTimeField(default=now)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
