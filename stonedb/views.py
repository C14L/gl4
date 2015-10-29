from django.conf import settings
# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response  # redirect, get_object_or_404
from django.template import RequestContext
# from django.views.decorators.http import require_http_methods


def home(request, t='stonedb/home.html', c={'settings': settings}):
    return render_to_response(t, c, context_instance=RequestContext(request))


def simple_filter(request, f, q, t='stonedb/simple_filter.html', c={}):
    """Return a list of stones for one filter, e.g. color.

    Example: /stone/color/blue
    """
    return render_to_response(t, c, context_instance=RequestContext(request))


def filter(request, q, t='stonedb/filter.html', c={}):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/blue-sandstone-from-france
    """
    return render_to_response(t, c, context_instance=RequestContext(request))
