from datetime import datetime

import pytz
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from stonedb.models import Color, Country, Classification, Texture


def add_search_mask_options(request):
    return {
        'search_colors': Color.objects.all_with_stones(),
        'search_countries': Country.objects.all_with_stones(),
        'search_classifications': Classification.objects.all_with_stones(),
        'search_textures': Texture.objects.all_with_stones(),
    }


def add_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'PRODUCTION': settings.PRODUCTION,
        'now_utc': datetime.now().replace(tzinfo=pytz.utc),
        'settings': settings,
    }


def add_common_translations(request):
    """Add some often used translations, less trans and blocktrans fiddling"""
    return {
        # Used in filter and simple_filter to build URLs.
        'tr_country': _('country'),
        'tr_color': _('country'),
        'tr_texture': _('country'),
        'tr_classification': _('classification'),
        'tr_type': _('type'),
    }
