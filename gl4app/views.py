from django.contrib.auth.models import User
from django.shortcuts import render

from companydb.models import Stock, Project
from allauth.account.views import SignupView, LoginView


class MySignupView(SignupView):
    template_name = 'account/my_signup.html'


class MyLoginView(LoginView):
    template_name = 'account/my_login.html'


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
    return render(request, 'gl4app/home.html', {
        'stocks': stocks, 'projects': projects, 'view_users': view_users})
