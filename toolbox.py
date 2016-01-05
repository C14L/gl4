"""Collection of random simple general-purpose helper functions."""

import dateutil.parser
import math
import pytz
import re

from datetime import date, datetime
from PIL import Image, ImageFont, ImageDraw
from django.conf import settings
# from typing import Union --> Py3.5

from django.utils.timezone import utc


def resize_copy(raw_fname: str, target_fname: str, resize_type: str,
                max_w: int, max_h: int, watermark: bool=None) -> bool:
    """
    Make a resized JPEG copy of the image with file name "raw_fname" and write
    the resulting image data to a file named "target_fname".

    The resulting image will be not larger than "max_w x max_h" pixels and is
    resized to either "contain" the original image completely and have some
    empty areas on the target image, or to "cover" the target image completely
    by cropping parts of the original image.

    :param raw_fname: Full file name of raw image.
    :param target_fname: Full file name of target image.
    :param resize_type: Either "cover" or "contain", like CSS3.
    :param max_w: Maximum width of target image.
    :param max_h: Maximum height of target image.
    :param watermark: Optional. If True, add settings.SITE_NAME as watermark.
    """
    file_type = 'JPEG'
    # raw_fh.seek(0)
    im = Image.open(raw_fname).convert('RGBA')

    # Original image size.
    curr_w, curr_h = im.size

    # Resize either "cover" or "contain".
    if resize_type == 'cover':
        # Same as CSS3, cover the entire target image and crop
        w = int(max_w)
        h = int(max(curr_h * max_w / curr_w, 1))
        cx2, cy2 = 0, int((h - max_h) / 2)  # part to crop
        if h < max_h:
            h = int(max_h)
            w = int(max(curr_w * max_h / curr_h, 1))
            cx2, cy2 = int((w - max_w) / 2), 0  # part to crop
        im = im.resize((w, h), Image.ANTIALIAS).crop((cx2, cy2, w-cx2, h-cy2))
        im.load()  # load() is necessary after crop

    elif resize_type == 'contain':
        # First calc to fit the width. Then check to see if height is still
        # too large, and if so, calc again to fit height.
        #
        # max_w, max_h: this is the target.
        # curr_w, curr_h: this is the current situation.
        if curr_w > max_w:
            curr_h = int(max(curr_h * max_w / curr_w, 1))
            curr_w = int(max_w)
        if curr_h > max_h:
            curr_w = int(max(curr_w * max_h / curr_h, 1))
            curr_h = int(max_h)
        im = im.resize((curr_w, curr_h), Image.ANTIALIAS)

    else:
        raise ValueError('No such resize_type "{}".'.format(resize_type))

    if watermark:
        font_fname = getattr(settings, 'WATERMARK_FONT_FILENAME',
                             '/usr/share/fonts/truetype/freefont/FreeSans.ttf')
        txt = settings.SITE_NAME
        font = ImageFont.truetype(font_fname, 16)
        im_tx_dark = Image.new('RGBA', im.size, (32, 32, 32, 0))
        im_tx_light = Image.new('RGBA', im.size, (255, 255, 255, 0))
        draw_ctx_dark = ImageDraw.Draw(im_tx_dark)
        draw_ctx_light = ImageDraw.Draw(im_tx_light)
        draw_ctx_dark.text((12, 12), txt, font=font, fill=(32, 32, 32, 192))
        draw_ctx_light.text((10, 10), txt, font=font, fill=(255, 255, 255, 192))
        im = Image.alpha_composite(im, im_tx_dark)
        im = Image.alpha_composite(im, im_tx_light)

    im.save(target_fname, file_type)
    return True


def to_iso8601(when: datetime=None) -> str:
    """
    Return a datetime as string in ISO-8601 format. If no time given, default
    to now.
    :param when:
    """
    if not when:
        when = datetime.now(pytz.utc)
    if not when.tzinfo:
        when = pytz.utc.localize(when)
    _when = when.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    return _when


def from_iso8601(when: str=None) -> datetime:
    """
    Return a UTC timezone aware datetime object from a string in ISO-8601
    format. If no time given, default to now.
    :param when:
    """
    if not when:
        _when = datetime.now(pytz.utc)
    else:
        _when = dateutil.parser.parse(when)
    if not _when.tzinfo:
        _when = pytz.utc.localize(_when)
    return _when


def parse_iso_datetime(t: str=None) -> datetime:
    """
    Return ISO timezone aware datetime from simple 'yyyy-mm-dd hh-mm-ss'.
    :param t:
    """
    if t:
        try:
            return datetime.strptime(t, "%Y-%m-%d %H:%M:%S").replace(tzinfo=utc)
        except ValueError:
            return None
    else:
        return datetime.utcnow().replace(tzinfo=utc)


def parse_iso_date(t: str=None) -> datetime:
    """
    Return timezone aware date from simple 'yyyy-mm-dd'.
    :param t:
    """
    if t:
        try:
            return datetime.strptime(t, "%Y-%m-%d").date()
        except ValueError:
            return None
    else:
        return date.today()


def force_int(x, min: int=None, max: int=None) -> int:
    """
    Receives any value and returns an integer. Values that can not be
    parsed are returned as 0. Values that are smaller that min or
    larger than max, if either is given, are set to min or max
    respectively.
    :param x:
    :param min:
    :param max:
    """
    try:
        i = int(x)
    except:
        return 0
    if min and i < min:
        i = min
    if max and i > max:
        i = max
    return i


def force_float(x) -> float:
    """
    Receives any value and returns a float. Values that can not be
    parsed are returned as 0.0
    :param x:
    """
    try:
        return float(x)
    except:
        return 0.0


def set_imgur_url(url: str, size: str='t') -> str:
    """
    Gets a imgur picture URL (e.g. "http://i.imgur.com/wPqDiEyl.jpg")
    and changes the size byte to 'size':
      - "s" small rectangular
      - "t" thumb
      - "m" medium
      - "l" large
      - "" original upload size

    If 'url' is not a valid imgur.com URL, the value is returned
    unchanged.
    :param url:
    :param size:
    """
    re_imgur_url = (r'(?P<base>https?://i.imgur.com/)'
                    r'(?P<name>[a-zA-Z0-9]{2,20}?)'
                    r'(?P<size>[stml]?)\.'
                    r'(?P<ext>jpe?g|gif|png|webp)')
    m = re.search(re_imgur_url, url)
    if m:
        url = '{}{}{}.{}'.format(m.group('base'), m.group('name'),
                                 size, m.group('ext'))
    return url


def get_imgur_page_from_picture_url(url: str) -> str:
    """
    Returns the URL of the containing page for a picture URL
    on imgur.com
    :param url:
    """
    re_imgur_url = (r'(?P<base>https?://i.imgur.com/)'
                    r'(?P<name>[a-zA-Z0-9]{2,20})'
                    r'(?P<size>[stml]?)\.'
                    r'(?P<ext>jpe?g|gif|png|webp)')
    m = re.search(re_imgur_url, url)
    if m:
        base = m.group('base').replace('i.', '')
        return '{}{}'.format(base, m.group('name'))
    else:
        return ''


# --- Date of Birth and Zodiac -------------------------------------- #


def get_dob_range(minage, maxage):
    """Return earliest and latest dob to match a min/max age range.
    :param minage:
    :param maxage:
    """
    year = date.today().year
    dob_earliest = date.today().replace(year=(year-maxage))
    dob_latest = date.today().replace(year=(year-minage))
    return dob_earliest, dob_latest


WESTERN_ZODIAC = (
    (0, ''), (1, 'aries'), (2, 'taurus'), (3, 'gemini'),
    (4, 'cancer'), (5, 'leo'), (6, 'virgo'), (7, 'libra'), (8, 'scorpio'),
    (9, 'sagittarius'), (10, 'capricorn'), (11, 'aquarius'), (12, 'pisces'))

WESTERN_ZODIAC_SYMBOLS = (
    (1, '♈'), (2, '♉'), (3, '♊'), (4,  '♋'), (5,  '♌'), (6,  '♍'),
    (7, '♎'), (8, '♏'), (9, '♐'), (10, '♑'), (11, '♒'), (12, '♓'))

WESTERN_ZODIAC_UPPER_LIMIT = (
    (120, 10), (218, 11), (320, 12), (420, 1), (521, 2), (621, 3), (722, 4),
    (823, 5), (923, 6), (1023, 7), (1122, 8), (1222, 9), (1231, 10))

EASTERN_ZODIAC = (
    (0, ''), (1, 'rat'), (2, 'ox'), (3, 'tiger'), (4, 'rabbit'),
    (5, 'dragon'), (6, 'snake'), (7, 'horse'), (8, 'goat'),
    (9, 'monkey'), (10, 'rooster'), (11, 'dog'), (12, 'pig'))

EASTERN_ZODIAC_SYMBOLS = (
    (1, '鼠'), (2, '牛'), (3, '虎'), (4, '兔'), (5, '龍'), (6, '蛇'),
    (7, '馬'), (8, '羊'), (9, '猴'), (10, '鷄'), (11, '狗'), (12, '猪'))

EASTERN_ZODIAC_UPPER_LIMIT = (  # from 1925-01-23 until 2044-01-29
    (19250123, 1), (19260212,  2), (19270201,  3), (19280122,  4),
    (19290209, 5), (19300129,  6), (19310216,  7), (19320205,  8),
    (19330125, 9), (19340213, 10), (19350203, 11), (19360123, 12),
    (19370210, 1), (19380130,  2), (19390218,  3), (19400207,  4),
    (19410126, 5), (19420214,  6), (19430204,  7), (19440124,  8),
    (19450212, 9), (19460201, 10), (19470127, 11), (19480209, 12),
    (19490128, 1), (19500216,  2), (19510205,  3), (19520126,  4),
    (19530213, 5), (19540202,  6), (19550123,  7), (19560211,  8),
    (19570130, 9), (19580217, 10), (19590207, 11), (19600127, 12),
    (19610214, 1), (19620204,  2), (19630124,  3), (19640212,  4),
    (19650201, 5), (19660120,  6), (19670208,  7), (19680129,  8),
    (19690216, 9), (19700205, 10), (19710126, 11), (19720214, 12),
    (19730202, 1), (19740122,  2), (19750210,  3), (19760130,  4),
    (19770217, 5), (19780206,  6), (19790127,  7), (19800215,  8),
    (19810204, 9), (19820124, 10), (19830212, 11), (19840201, 12),
    (19850219, 1), (19860208,  2), (19870128,  3), (19880216,  4),
    (19890205, 5), (19900126,  6), (19910214,  7), (19920203,  8),
    (19930122, 9), (19940209, 10), (19950130, 11), (19960218, 12),
    (19970206, 1), (19980127,  2), (19990215,  3), (20000204,  4),
    (20010123, 5), (20020211,  6), (20030131,  7), (20040121,  8),
    (20050208, 9), (20060128, 10), (20070217, 11), (20080206, 12),
    (20090125, 1), (20100213,  2), (20110202,  3), (20120122,  4),
    (20130209, 5), (20140130,  6), (20150218,  7), (20160207,  8),
    (20170127, 9), (20180215, 10), (20190204, 11), (20200124, 12),
    (20210211, 1), (20220131,  2), (20230121,  3), (20240209,  4),
    (20250128, 5), (20260216,  6), (20270205,  7), (20280125,  8),
    (20290212, 9), (20300202, 10), (20310122, 11), (20320210, 12),
    (20330130, 1), (20340218,  2), (20350207,  3), (20360127,  4),
    (20370214, 5), (20380203,  6), (20390123,  7), (20400211,  8),
    (20410131, 9), (20420121, 10), (20430209, 11), (20440129, 12))


def _get_western_zodiac_index(dob):
    """Gets a datetime.date value and returns its Western zodiac index
    :param dob:
    """
    try:
        mdd = int(dob.strftime('%m%d'))
        lim = WESTERN_ZODIAC_UPPER_LIMIT
        return [e[1] for e in lim if mdd < e[0]][0]
    except:
        return 0


def get_western_zodiac(dob):
    try:
        return WESTERN_ZODIAC[_get_western_zodiac_index(dob)][1]
    except IndexError:
        return ''


def get_western_zodiac_symbol(dob):
    try:
        return WESTERN_ZODIAC_SYMBOLS[_get_western_zodiac_index(dob)][1]
    except IndexError:
        return ''


def get_eastern_zodiac_index(dob):
    """Gets a datetime.date value and returns its Eastern zodiac
    :param dob:
    """
    try:
        ymd = int(dob.strftime('%Y%m%d'))
        lim = EASTERN_ZODIAC_UPPER_LIMIT
        return [e[1] for e in lim if ymd < e[0]][0]
    except:
        return 0


def get_eastern_zodiac(dob):
    try:
        return EASTERN_ZODIAC[get_eastern_zodiac_index(dob)][1]
    except IndexError:
        return ''


def get_eastern_zodiac_symbol(dob):
    try:
        return EASTERN_ZODIAC_SYMBOLS[get_eastern_zodiac_index(dob)][1]
    except IndexError:
        return ''


# --- Geolocation --------------------------------------------------- #


def distance_between_geolocations(p1, p2):
    """
    Gets two geolocation points p1 and p2 as (lat, lng) tuples. Returns
    the approximate distance in meters. Does not account for earth's
    curvature, so that inaccuracy increases with distance.
    :param p1:
    :param p2:
    """
    p1_lat, p1_lng = float(p1[0]), float(p1[1])
    p2_lat, p2_lng = float(p2[0]), float(p2[1])
    lat_1_deg = 110574.0  # 1 deg lat in meters (m)
    p1_lng_1_deg = 111320.0 * math.cos(p1_lat)  # 1 deg lng in m for p1_lat
    p2_lng_1_deg = 111320.0 * math.cos(p2_lat)  # 1 deg lng in m for p2_lat
    lng_1_deg = (p1_lng_1_deg + p2_lng_1_deg) / 2  # average them
    lat_delta_m = (p1_lat - p2_lat) * lat_1_deg
    lng_delta_m = (p1_lng - p2_lng) * lng_1_deg
    return int(math.sqrt(math.pow(lat_delta_m, 2) + math.pow(lng_delta_m, 2)))


def get_latlng_bounderies(lat, lng, distance):
    """Return min/max lat/lng values for a distance around a latlng.

    Receives a geolocation as lat/lng floats and a distance (km) around
    that point. To simplify database lookup, only get a square around
    the geolocation. Return (lat_min, lng_min) and (lat_max, lng_max)
    geolocation points to draw the box.
    :param lat:
    :param lng:
    :param distance:
    """
    lat_1deg = 110574.0  # m
    lng_1deg = 111320.0 * math.cos(lat)  # m
    dist_m = float(distance * 1000)
    lat_dist_deg = abs(dist_m / lat_1deg)
    lng_dist_deg = abs(dist_m / lng_1deg)
    return (lat-lat_dist_deg, lng-lat_dist_deg,
            lat+lng_dist_deg, lng+lng_dist_deg)


# ------------------------------------------------------------------- #
