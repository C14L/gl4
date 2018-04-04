import time
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render

from companydb.models import Stock, Project


def home(request):
    __t = [time.time()]

    view_users = list(
        User.objects
            .prefetch_related('profile')
            .exclude(profile__city='')
            .exclude(profile__country_name='')
            .filter(profile__title_foto__gt=0)
            .filter(profile__is_blocked=False)
            .filter(profile__is_deleted=False)
            .order_by('-last_login', '-pk')[:10])

    __t.append(time.time())

    # NotImplementedError: annotate() + distinct(fields) is not implemented.
    # stocks = Stock.objects.all_public().order_by('user').distinct('user')\
    #                                    .order_by('-created')[:10]
    stocks = []
    for item in Stock.objects.all_public()[:100]:
        if item.user.id not in [x.user.id for x in stocks]:
            stocks.append(item)
        if len(stocks) >= 10:
            break

    __t.append(time.time())

    projects = list(Project.objects.all_public()[:10])

    __t.append(time.time())

    ret = render(request, 'gl4app/home.html', {
        'stocks': stocks,
        'projects': projects,
        'view_users': view_users})

    __t.append(time.time())

    if 'timer' in request.GET:
        __diff = [__t[i] - __t[i - 1] for i in range(1, len(__t))]
        x_diff = [str(int(x * 100) / 100) for x in __diff]
        return HttpResponse(' # '.join(x_diff))
    else:
        return ret


def user_home(request):
    url = reverse('home')
    if request.user.is_authenticated():
        url = reverse('companydb_item', args=[request.user.username])
    return HttpResponsePermanentRedirect(url)
