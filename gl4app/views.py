from django.contrib.auth.models import User
from django.shortcuts import render_to_response as rtr
from django.template import RequestContext
from companydb.models import Stock, Project


def home(request):
    view_users = User.objects.filter(is_active=True)\
                     .exclude(last_login__isnull=True)\
                     .exclude(profile__title_foto=0)\
                     .exclude(profile__city='')\
                     .exclude(profile__country_name='')\
                     .exclude(profile__is_blocked=True)\
                     .exclude(profile__is_deleted=True)\
                     .order_by('last_login')[:10]

    stocks = []
    # NotImplementedError: annotate() + distinct(fields) is not implemented.
    # stocks = Stock.objects.all_public().order_by('user').distinct('user')\
    #                                    .order_by('-created')[:10]
    for item in Stock.objects.all_public()[:500]:
        if item.user.id not in [x.user.id for x in stocks]:
            stocks.append(item)
        if len(stocks) >= 10:
            break

    projects = Project.objects.all_public()[:10]

    tpl = 'gl4app/home.html'
    ctx = {'stocks': stocks, 'projects': projects, 'view_users': view_users}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
