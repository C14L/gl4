from django.conf import settings
from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from os.path import join

register = template.Library()


@register.filter
def keyvalue(dic, key):
    """Use a variable as a dictionary key"""
    return dic[key]


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


@register.simple_tag(name='adsense')
def adsense_tag(slot, name):
    # All ad names start with "gc" (graniteland.com) or "gd" (graniteland.de)
    client = settings.ADSENSE_AD_CLIENT
    gcgd, clss = name.split(' ', 1)
    clss = slugify(clss)

    # Only display the correct ads (gd or gc) depending on LANGUAGE_CODE.
    if gcgd == 'gc' and not settings.LANGUAGE_CODE.startswith('en'):
        return ''
    if gcgd == 'gd' and not settings.LANGUAGE_CODE.startswith('de'):
        return ''

    if settings.PRODUCTION:
        params = {'gcgd': gcgd, 'clss': clss,
                  'client': client, 'slot': slot, 'name': name}
        html = '''
<div class="ads {gcgd} {clss}">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- {name} -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="{client}"
     data-ad-slot="{slot}"
     data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script></div>'''
    else:
        params = {'gcgd': gcgd, 'clss': clss, 'name': name}
        html = '''<div class="fake ads {gcgd} {clss}"><div>{name}</div></div>'''

    return mark_safe(html.format(**params))
