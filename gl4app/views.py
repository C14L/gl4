from django.shortcuts import render_to_response as rtr
from django.template import RequestContext


def home(request):
    tpl = 'gl4app/home.html'
    ctx = {}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
