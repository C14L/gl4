import pytz
from datetime import datetime
from django.conf import settings
from stonedb.models import Color, Country


def add_search_mask_options(request):
    return {
        'search_colors': Color.objects.all_with_stones(),
        'search_countries': Country.objects.all_with_stones(),
    }


def add_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'PRODUCTION': settings.PRODUCTION,
        'now_utc': datetime.now().replace(tzinfo=pytz.utc),
        'settings': settings,
    }
