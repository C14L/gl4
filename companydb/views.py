from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rtr
from django.template import RequestContext
from companydb.models import Group, Pic, Stock, Project
from stonedb.models import Stone


def get_page(o, p):
    PER_PAGE = getattr(settings, 'PER_PAGE', 20)
    paginator = Paginator(o, PER_PAGE)
    return paginator.page(p)


def home(request):
    tpl = 'companydb/home.html'
    ctx = {'groups': Group.objects.all()}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def list(request, slug, p):
    group = get_object_or_404(Group, slug=slug)
    members_qs = group.members.filter(is_active=True,
                                      profile__is_deleted=False,
                                      profile__is_blocked=False)
    members_qs = members_qs.prefetch_related('profile')
    members_qs = members_qs.order_by('profile__name')
    members = get_page(members_qs, p)

    tpl = 'companydb/list.html'
    ctx = {'group': group, 'members': members,
           'range_pages': range(1, members.paginator.num_pages+1)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def item(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    pics = Pic.objects.filter(user=view_user, module='profile')
    tpl = 'companydb/item.html'
    ctx = {'view_user': view_user, 'pics': pics}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def stock(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    all = view_user.stock_set.filter(is_deleted=False, is_blocked=False)
    tpl = 'companydb/stock.html'
    ctx = {'view_user': view_user, 'stock': get_page(all, page)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def projects(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    all = view_user.project_set.filter(is_deleted=False, is_blocked=False)
    tpl = 'companydb/projects.html'
    ctx = {'view_user': view_user, 'projects': get_page(all, page)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def photos(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    all = Pic.objects.filter(module='profile', user=view_user)\
                    .exclude(is_blocked=True, is_deleted=True)
    tpl = 'companydb/photos.html'
    ctx = {'view_user': view_user, 'photos': get_page(all, page)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def contact(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    tpl = 'companydb/contact.html'
    ctx = {'view_user': view_user}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def photo_redir(request, slug, id):
    pic = get_object_or_404(Pic, pk=id)
    url = reverse('companydb_pic_item', kwargs={'id': pic.id})
    return HttpResponsePermanentRedirect(url)


def pic_item(request, id):
    pic = get_object_or_404(Pic, pk=id)
    related = None
    # Get the related module objects that this pic is atatched to.
    if pic.module == 'stones':
        related = get_object_or_404(Stone, pk=pic.module_id)
    elif pic.module == 'projects':
        related = get_object_or_404(Project, pk=pic.module_id)
    elif pic.module == 'stock':
        related = get_object_or_404(Stock, pk=pic.module_id)
    elif pic.module == 'groups':
        related = get_object_or_404(Group, pk=pic.module_id)
    elif pic.module == 'pages':
        related = get_object_or_404(Pages, pk=pic.module_id)

    tpl = 'companydb/pic_item.html'
    ctx = {'pic': pic, 'related': related, 'view_user': pic.user}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def dashboard(request):

    tpl = 'companydb/dashboard.html'
    ctx = {}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
