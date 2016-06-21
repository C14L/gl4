from django.contrib.auth.models import User
from django.shortcuts import render

from companydb.models import Stock, Project


def home(request):
    view_users = User.objects.filter(is_active=True)\
                     .filter(last_login__isnull=False)\
                     .filter(profile__title_foto__gt=0)\
                     .exclude(profile__city='')\
                     .exclude(profile__country_name='')\
                     .filter(profile__is_blocked=False)\
                     .filter(profile__is_deleted=False)\
                     .prefetch_related('profile')\
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
    return render(request, 'gl4app/home.html', {
        'stocks': stocks, 'projects': projects, 'view_users': view_users})
