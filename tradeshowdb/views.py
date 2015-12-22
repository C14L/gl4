from datetime import date
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rtr
from django.template import RequestContext
from toolbox import force_int
from tradeshowdb.models import Tradeshow
from toolbox import parse_iso_date, parse_iso_datetime

def home(request, y=None):
    if y is None:
        url = reverse('tradeshowdb_by_year', kwargs={'y': date.today().year})
        return HttpResponsePermanentRedirect(url)

    view_year = force_int(y)
    tradeshows = Tradeshow.objects.filter(begins__year=view_year)
    ts_total = len(tradeshows)
    li = []  # sort them into per-month lists.
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    for a in months:
        idx = months.index(a) + 1
        tss = [b for b in tradeshows if b.begins.month == idx]
        li.append({'idx': idx, 'name': a, 'tradeshows': tss})

    tpl = 'tradeshowdb/home.html'
    ctx = {'years': range((view_year - 3), (view_year + 4)),
           'view_year': view_year, 'tradeshows': li, 'ts_total': ts_total}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def item(request, y, slug):
    year = force_int(y)
    tradeshow = get_object_or_404(Tradeshow, begins__year=year, url=slug)
    tpl = 'tradeshowdb/item.html'
    ctx = {'tradeshow': tradeshow, 'view_year': year}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
