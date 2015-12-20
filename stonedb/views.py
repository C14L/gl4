from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response as rtr
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from stonedb.models import Stone, Classification, Color, Country, Texture
from toolbox import force_int


FILTER_URL_NO_VALUE = 'all'
STONES_PER_PAGE = getattr(settings, 'STONES_PER_PAGE', 50)


def home(request):
    tpl = 'stonedb/home.html'
    ctx = {
        'classifications': Classification.objects.all_with_stones(),
        'colors': Color.objects.all_with_stones(),
        'countries': Country.objects.all_with_stones(),
        'textures': Texture.objects.all_with_stones(),
    }

    return rtr(tpl, ctx, context_instance=RequestContext(request))


@require_http_methods(["GET"])
def redir_search_php(request):
    # /stone/search.php?p=1&color=&country=&classification=13&pseu=
    #  -->
    # /stone/france/coarse-grained/blue/sandstone
    p = force_int(request.GET.get('p', 1))
    color = force_int(request.GET.get('color', 0))
    country = force_int(request.GET.get('country', 0))
    texture = force_int(request.GET.get('texture', 0))
    classif = force_int(request.GET.get('classification', 0))

    if color:
        color = get_object_or_404(Color, pk=color)
    if country:
        country = get_object_or_404(Country, pk=country)
    if texture:
        texture = get_object_or_404(Texture, pk=texture)
    if classif:
        classif = get_object_or_404(Classification, pk=classif)

    # Now redirect depending on what values we received.
    if not (color or country or texture or classif):
        # no vals at all?!
        url = reverse('stonedb_home')
    elif color and not (country or texture or classif):
        # only color
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'color', 'q': color.slug})
    elif country and not (color or texture or classif):
        # only country
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'country', 'q': country.slug})
    elif texture and not (color or country or classif):
        # only texture
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'texture', 'q': texture.slug})
    elif classif and not (color or country or texture):
        # only classification
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'classif', 'q': classif.slug})
    else:
        # if there are at least two properties defined, then show filter page.
        url = reverse('stonedb_filter', kwargs={
            'color': getattr(color, 'slug', FILTER_URL_NO_VALUE),
            'country': getattr(country, 'slug', FILTER_URL_NO_VALUE),
            'texture': getattr(texture, 'slug', FILTER_URL_NO_VALUE),
            'classif': getattr(classif, 'slug', FILTER_URL_NO_VALUE)})
        if p > 1:
            url['p'] = p

    return HttpResponsePermanentRedirect(url)


def property_list(request, f):
    """
    Simple links page with links to all "colors" or all "countries".

    f -> filter (color, country, type)

    Example: /stone/color
             /stone/country
             /stone/type
             /stone/texture
    """
    f = f.lower()
    fk = f

    if f == 'color':
        li = Color.objects.all_with_stones()
    elif f == 'country':
        li = Country.objects.all_with_stones()
    elif f == 'texture':
        li = Texture.objects.all_with_stones()
    elif f == 'type':
        li = Classification.objects.all_with_stones()
        fk = 'classification'
    else:
        raise Http404

    tpl = 'stonedb/property_list.html'
    ctx = {'items': li, 'f': f, 'fk': fk}

    return rtr(tpl, ctx, context_instance=RequestContext(request))


def simple_filter(request, f, q, p):
    """Return a list of stones for one filter, e.g. color.

    f -> filter (color, country, type)
    q -> query (color name, etc.)
    p -> page number (always None for page 1)

    Example: /stone/color/blue/
    """
    p = p or 1  # no page number means page 1
    f = f.lower()
    fk = f  # filter "type" needs "classification" as filter key

    if f == 'color':
        more = Color.objects.all_with_stones()
        q = get_object_or_404(Color, slug=q)
    elif f == 'country':
        more = Country.objects.all_with_stones()
        q = get_object_or_404(Country, slug=q)
    elif f == 'texture':
        more = Texture.objects.all_with_stones()
        q = get_object_or_404(Texture, slug=q)
    elif f == 'type':
        more = Classification.objects.all_with_stones()
        fk = 'classification'
        q = get_object_or_404(Classification, slug=q)
    else:
        raise Http404

    paginator = Paginator(Stone.objects.filter(**{fk: q}), STONES_PER_PAGE)

    tpl = 'stonedb/filter_{}.html'.format(fk)
    ctx = {'stones': paginator.page(p), 'f': f, 'q': q, 'more': more}

    return rtr(tpl, ctx, context_instance=RequestContext(request))


def filter(request, color, country, texture, classif, p=1):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/sandstone/blue/veined/france/
    """
    p = force_int(p) or 1
    color = request.GET.get('color', FILTER_URL_NO_VALUE).lower()
    country = request.GET.get('country', FILTER_URL_NO_VALUE).lower()
    texture = request.GET.get('texture', FILTER_URL_NO_VALUE).lower()
    classif = request.GET.get('classif', FILTER_URL_NO_VALUE).lower()

    li = Stone.objects.all()

    if color != FILTER_URL_NO_VALUE:
        color = Color.objects.get(slug=color)
        li = li.filter(color=color)
    if country != FILTER_URL_NO_VALUE:
        country = Country.objects.get(slug=country)
        li = li.filter(country=country)
    if texture != FILTER_URL_NO_VALUE:
        texture = Texture.objects.get(slug=texture)
        li = li.filter(texture=texture)
    if classif != FILTER_URL_NO_VALUE:
        classif = Classification.objects.get(slug=classif)
        li = li.filter(classification=classif)

    paginator = Paginator(li, STONES_PER_PAGE)
    tpl = 'stonedb/filter.html'
    ctx = {'stones': paginator.page(p),
           'color': color,
           'country': country,
           'texture': texture,
           'classification': classif}

    return rtr(tpl, ctx, context_instance=RequestContext(request))


def item(request, q):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    stone = get_object_or_404(Stone, slug=q)
    tpl = 'stonedb/item.html'
    ctx = {'stone': stone}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
