from django.conf import settings
from django.core.paginator import Paginator
# from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404  # redirect
from django.template import RequestContext
# from django.views.decorators.http import require_http_methods
from stonedb.models import Stone, Classification, Color, Country, Texture


def home(request):
    template_file = 'stonedb/home.html'
    context = {'settings': settings}
    return render_to_response(template_file, context,
                              context_instance=RequestContext(request))


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

    try:
        if f == 'color':
            q = get_object_or_404(Color, slug=q)
            template_file = 'stonedb/filter_color.html'
        elif f == 'country':
            q = get_object_or_404(Country, slug=q)
            template_file = 'stonedb/filter_country.html'
        elif f == 'texture':
            q = get_object_or_404(Texture, slug=q)
            template_file = 'stonedb/filter_texture.html'
        elif f == 'type':
            fk = 'classification'
            q = get_object_or_404(Classification, slug=q)
            template_file = 'stonedb/filter_classification.html'
    except IndexError:
        raise Http404

    paginator = Paginator(Stone.objects.filter(**{fk: q}), STONES_PER_PAGE)
    context = {'stones': paginator.page(p), 'f': f, 'q': q}
    return render_to_response(template_file, context,
                              context_instance=RequestContext(request))


def filter(request, q):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    template_file = 'stonedb/filter.html'
    context = {}
    return render_to_response(template_file, context,
                              context_instance=RequestContext(request))


def item(request, q):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    stone = get_object_or_404(Stone, slug=q)
    template_file = 'stonedb/item.html'
    context = {'stone': stone, 'settings': settings}
    return render_to_response(template_file, context,
                              context_instance=RequestContext(request))
