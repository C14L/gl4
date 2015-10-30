from django.conf import settings
from django.shortcuts import render_to_response  # redirect, get_object_or_404
from django.template import RequestContext
# from django.views.decorators.http import require_http_methods


def home(request, t='home.html', c={'settings': settings}):
    return render_to_response(t, c, context_instance=RequestContext(request))
