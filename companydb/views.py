from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rtr
from django.template import RequestContext
from companydb.models import Group


def home(request):
    tpl = 'companydb/home.html'
    ctx = {'groups': Group.objects.all()}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def list(request, slug, p):
    PER_PAGE = getattr(settings, 'PER_PAGE', 20)
    group = get_object_or_404(Group, slug=slug)
    members_qs = group.members.filter(is_active=True,
                                      profile__is_deleted=False,
                                      profile__is_blocked=False)
    members_qs = members_qs.prefetch_related('profile')
    members_qs = members_qs.order_by('profile__name')
    members_all = Paginator(members_qs, PER_PAGE)
    members_page = members_all.page(p)

    tpl = 'companydb/list.html'
    ctx = {'group': group, 'members': members_page,
           'range_pages': range(1, members_all.num_pages+1)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def item(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    tpl = 'companydb/item.html'
    ctx = {'view_user': view_user}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
