from datetime import datetime

import pytz
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext as _

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
        'active_language': get_language(),
    }


def add_common_translations(request):
    """Add some often used translations, less trans and blocktrans fiddling.
    Used in filter and simple_filter to build URLs."""

    return {
        'footer_browse_stones': {
            settings.TR_COLOR: (
                (_('beige'),  _('Beige natural stone')),
                (_('black'),  _('Black natural stone')),
                (_('blue'),   _('Blue natural stone')),
                (_('brown'),  _('Brown natural stone')),
                (_('green'),  _('Green natural stone')),
                (_('grey'),   _('Grey natural stone')),
                (_('pink'),   _('Pink natural stone')),
                (_('red'),    _('Red natural stone')),
                (_('white'),  _('White natural stone')),
                (_('yellow'), _('Yellow natural stone')),
            ),
            settings.TR_COUNTRY: (
                (_('Brazil').lower(),  _('Granite and marble from Brazil')),
                (_('China').lower(),   _('Granite and marble from China')),
                (_('Germany').lower(), _('Granite and marble from Germany')),
                (_('France').lower(),  _('Granite and marble from France')),
                (_('India').lower(),   _('Granite and marble from India')),
                (_('Italy').lower(),   _('Granite and marble from Italy')),
                (_('Spain').lower(),   _('Granite and marble from Spain')),
            ),
            settings.TR_TYPE: (
                (_('granite').lower(), _('Granite')),
                (_('limestone').lower(), _('Limestone')),
                (_('marble').lower(), _('Marble')),
                (_('quartzite').lower(), _('Quartzite')),
                (_('sandstone').lower(), _('Sandstone')),
                (_('slate').lower(), _('Slate')),
                (_('soapstone').lower(), _('Soapstone')),
                (_('travertine').lower(), _('Travertine')),
            ),
        },
        'tr_country': settings.TR_COUNTRY,
        'tr_color': settings.TR_COLOR,
        'tr_texture': settings.TR_TEXTURE,
        'tr_classification': settings.TR_CLASSIFICATION,
        'tr_type': settings.TR_TYPE,

        'tr_mdpages_home': settings.TR_MDPAGES_HOME,
        'tr_mdpages_professional': settings.TR_MDPAGES_PROFESSIONAL,
        'tr_mdpages_production': settings.TR_MDPAGES_PRODUCTION,
        'tr_mdpages_misc': settings.TR_MDPAGES_MISC,
        'tr_mdpages_help': settings.TR_MDPAGES_HELP,
    }
