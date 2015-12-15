import pytz
from datetime import datetime
from django.conf import settings


def add_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'PRODUCTION': settings.PRODUCTION,
        'now_utc': datetime.now().replace(tzinfo=pytz.utc),
        'settings': settings,
    }
