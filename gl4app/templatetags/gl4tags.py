from django.conf import settings
from django import template
from os.path import join

register = template.Library()


@register.filter(name='picsrc')
def picsrc(pic, size='small'):
    """Return the URL to a user uploaded media file in a give size."""
    picfile = '{}.{}'.format(pic.id, pic.ext)
    sizedir = 'fotos_{}'.format(size)
    return join(settings.MEDIA_URL, sizedir, picfile)
