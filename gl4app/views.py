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
                     .order_by('-last_login')

    tpl = 'gl4app/home.html'
    ctx = {'stocks': Stock.objects.all_public()[:10],
           'projects': Project.objects.all_public()[:10],
           'view_users': view_users[:10], }
    return rtr(tpl, ctx, context_instance=RequestContext(request))
