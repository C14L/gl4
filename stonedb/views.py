from django.conf import settings
from django.core.paginator import Paginator
# from django.http import Http404
from django.shortcuts import render_to_response as rtr
from django.shortcuts import get_object_or_404
from django.template import RequestContext
# from django.views.decorators.http import require_http_methods
from stonedb.models import Stone, Classification, Color, Country, Texture


def home(request):
    tpl = 'stonedb/home.html'
    ctx = {
        'classifications': Classification.objects.all_with_stones(),
        'colors': Color.objects.all_with_stones(),
        'countries': Country.objects.all_with_stones(),
        'textures': Texture.objects.all_with_stones(),
    }

    return rtr(tpl, ctx, context_instance=RequestContext(request))


def simple_filter(request, f, q, p):
    """Return a list of stones for one filter, e.g. color.

    f -> filter (color, country, type)
    q -> query (color name, etc.)
    p -> page number (always None for page 1)

    Example: /stone/color/blue/
    """
    STONES_PER_PAGE = getattr(settings, 'STONES_PER_PAGE', 50)
    p = p or 1  # no page number means page 1
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

    paginator = Paginator(Stone.objects.filter(**{fk: q}), STONES_PER_PAGE)

    tpl = 'stonedb/filter_{}.html'.format(fk)
    ctx = {'stones': paginator.page(p), 'f': f, 'q': q, 'more': more}

    return rtr(tpl, ctx, context_instance=RequestContext(request))


def filter(request, q):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/sandstone/blue/veined/france/
    """
    tpl = 'stonedb/filter.html'
    ctx = {}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def item(request, q):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    stone = get_object_or_404(Stone, slug=q)
    tpl = 'stonedb/item.html'
    ctx = {'stone': stone}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
