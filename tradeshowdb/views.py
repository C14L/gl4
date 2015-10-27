# from django.conf import settings
from django.http import HttpResponse


def home(request):
    return HttpResponse('tradeshowdb home')


def by_year(request, y):
    return HttpResponse('tradeshowdb by year {}'.format(y))


def item(request, y, slug):
    return HttpResponse('tradeshowdb item {}: {}'.format(y, slug))
