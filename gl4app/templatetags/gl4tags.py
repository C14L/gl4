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


@register.filter(name='fix_external_link')
def fix_external_link(href):
    """Make sure the external URL has a leading schema etc"""
    if not href.startswith('http'):
        href = 'http://' + href
    if href.startswith('http//'):
        href = 'http://' + href[6:]

    return href


@register.filter(name='iconpath')
def iconpath(slug):
    return join(settings.STATIC_URL, 'img/icons/nuovext22', slug + '.png')
