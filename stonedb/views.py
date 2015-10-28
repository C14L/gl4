# from django.conf import settings
# from django.core.urlresolvers import reverse
from django.http import HttpResponse  # HttpResponseNotFound
# from django.shortcuts import redirect, render_to_response, get_object_or_404
# from django.template import RequestContext
# from django.views.decorators.http import require_http_methods


def home(request):
    template_file = 'stonedb/home.html'
    return HttpResponse('Homepage')


def simple_filter(request, f, q):
    """Return a list of stones for one filter, e.g. color.

    Example: /stone/color/blue
    """
    template_file = 'stonedb/simple_filter.html'
    return HttpResponse('Simple Filter: {} > {}'.format(f, q))


def filter(request, q):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    template_file = 'stonedb/filter.html'
    return HttpResponse('Simple Filter: {}'.format(q))
