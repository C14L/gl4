from datetime import date

from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
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

    years = range((this_year - 1), (this_year + 4))
    ctx = {'years': years, 'view_year': view_year,
           'tradeshows': li, 'ts_total': ts_total}
    return render(request, 'tradeshowdb/home.html', ctx)


def item(request, y, slug):
    year = force_int(y)
    tradeshow = get_object_or_404(Tradeshow, begins__year=year, url=slug)
    ctx = {'tradeshow': tradeshow, 'view_year': year}
    return render(request, 'tradeshowdb/item.html', ctx)
