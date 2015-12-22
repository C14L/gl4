# from django.conf import settings
from django.http import HttpResponse


def home(request):
    return HttpResponse('companiesdb home')


def list(request, slug, p):
    return HttpResponse('companiesdb list')


def item(request, slug):
    return HttpResponse('companiesdb item')
