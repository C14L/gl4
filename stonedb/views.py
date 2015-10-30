from django.conf import settings
from django.core.paginator import Paginator
# from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response  # redirect, get_object_or_404
from django.template import RequestContext
# from django.views.decorators.http import require_http_methods
from .models import Stone


def home(request, t='stonedb/home.html', c={'settings': settings}):
    return render_to_response(t, c, context_instance=RequestContext(request))


def simple_filter(request, f, q, p=1):
    """Return a list of stones for one filter, e.g. color.

    f -> filter (color, country, type)
    q -> query (color name, etc.)
    p -> page

    Example: /stone/color/blue
    """
    if not (
        (f == 'color' and q in [x[1] for x in Stone.COLOR_CHOICES]) or
        (f == 'country' and q in [x[1] for x in Stone.COUNTRY_CHOICES]) or
        (f == 'type' and q in [x[1] for x in Stone.CLASSIFICATION_CHOICES])
    ):
        raise Http404

    stones = Paginator(Stone.objects.filter(**{f: q}), p)
    template_file = 'stonedb/simple_filter.html'
    context = {'stones': stones}
    return render_to_response(template_file,
                              context,
                              context_instance=RequestContext(request))


def filter(request, q, t='stonedb/filter.html', c={}):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    return render_to_response(t, c, context_instance=RequestContext(request))
