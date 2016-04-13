from datetime import date

from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404, render

from toolbox import force_int
from tradeshowdb.models import Tradeshow


def home(request, y=None):
    this_year = date.today().year
    view_year = force_int(y)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    if y is None:
        url = reverse('tradeshowdb_by_year', kwargs={'y': this_year})
        return HttpResponsePermanentRedirect(url)

    tradeshows = Tradeshow.objects.filter(begins__year=view_year)
    ts_total = len(tradeshows)
    li = []  # sort them into per-month lists.
    for a in months:
        idx = months.index(a) + 1
        tss = [b for b in tradeshows if b.begins.month == idx]
        li.append({'idx': idx, 'name': a, 'tradeshows': tss})

    return render(request, 'tradeshowdb/home.html', {
        'years': range((this_year-1), (this_year+4)), 'view_year': view_year,
        'tradeshows': li, 'ts_total': ts_total,
        'tpl_search_form': 'tradeshows'})


def item(request, y, slug):
    this_year = date.today().year
    year = force_int(y)
    tradeshow = Tradeshow.objects.filter(begins__year=year, url=slug).first()
    if not tradeshow:
        raise Http404()
    return render(request, 'tradeshowdb/item.html', {
        'years': range((this_year-1), (this_year+4)), 'tradeshow': tradeshow,
        'view_year': year, 'tpl_search_form': 'tradeshows'})
