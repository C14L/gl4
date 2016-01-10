from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, \
    HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rtr
from django.template import RequestContext

from companydb.forms import PicUploadForm, CompanyDetailsForm, \
    CompanyAboutForm, CompanyProjectForm
from companydb.models import Group, Pic, Stock, Project
from mdpages.models import Article
from stonedb.models import Stone


def _get_page(o, p):
    per_page = getattr(settings, 'PER_PAGE', 20)
    paginator = Paginator(o, per_page)
    return paginator.page(p)


def home(request):
    tpl = 'companydb/home.html'
    ctx = {'groups': Group.objects.all()}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def itemlist(request, slug, p):
    group = get_object_or_404(Group, slug=slug)
    members_qs = group.members.filter(is_active=True,
                                      profile__is_deleted=False,
                                      profile__is_blocked=False)
    members_qs = members_qs.prefetch_related('profile')
    members_qs = members_qs.order_by('profile__name')
    members = _get_page(members_qs, p)

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
    li = view_user.stock_set.filter(is_deleted=False, is_blocked=False)
    tpl = 'companydb/stock.html'
    ctx = {'view_user': view_user, 'stock': _get_page(li, page)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def projects(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = view_user.project_set.filter(is_deleted=False, is_blocked=False)
    tpl = 'companydb/projects.html'
    ctx = {'view_user': view_user, 'projects': _get_page(li, page)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def photos(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = Pic.objects.all_for_profile(view_user)
    tpl = 'companydb/photos.html'
    ctx = {'view_user': view_user, 'photos': _get_page(li, page)}
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
    # Get the related module objects that this pic is attached to.
    if pic.module == 'stones':
        related = get_object_or_404(Stone, pk=pic.module_id)
    elif pic.module == 'projects':
        related = get_object_or_404(Project, pk=pic.module_id)
    elif pic.module == 'stock':
        related = get_object_or_404(Stock, pk=pic.module_id)
    elif pic.module == 'groups':
        related = get_object_or_404(Group, pk=pic.module_id)
    elif pic.module == 'pages':
        related = get_object_or_404(Article, pk=pic.module_id)

    if request.user.is_authenticated():
        if "DELETE" in (request.method, request.POST.get('_method', None)):
            pic.delete()
            _next = request.POST.get('next', reverse('companydb_db_pics'))
            return HttpResponseRedirect(_next)

    tpl = 'companydb/pic_item.html'
    ctx = {'pic': pic, 'related': related, 'view_user': pic.user}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def dashboard(request):
    tpl = 'companydb/dashboard.html'
    ctx = {}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def db_details(request):
    if request.method == 'POST':
        form = CompanyDetailsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return HttpResponse()
            else:
                return HttpResponseRedirect(request.path)
    else:
        form = CompanyDetailsForm(instance=request.user.profile)

    tpl = 'companydb/db_details.html'
    ctx = {'form': form}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def db_about(request):
    if request.method == 'POST':
        form = CompanyAboutForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return HttpResponse()
            else:
                return HttpResponseRedirect(request.path)
    else:
        form = CompanyAboutForm(instance=request.user.profile)

    tpl = 'companydb/db_about.html'
    ctx = {'form': form}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def db_areas(request):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=request.POST.get('group', None))

        if request.POST.get('_method', None) == 'POST':
            # add a company to a group
            group.members.add(request.user.pk)
        elif request.POST.get('_method', None) == 'DELETE':
            # remove a company from a group
            group.members.remove(request.user.pk)

        if request.is_ajax():
            return HttpResponse()
        else:
            return HttpResponseRedirect(request.path)

    tpl = 'companydb/db_areas.html'
    ctx = {'groups': Group.objects.all()}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def db_pics(request):
    if request.method == 'POST':
        form = PicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pic = Pic.objects.add_to_profile(request.user,
                                             request.FILES['pic'],
                                             form.cleaned_data['title'])
            if request.is_ajax():
                return JsonResponse({'pic': {
                    'url_thumb': pic.url_thumb,
                    'url_small': pic.url_small,
                    'url_medium': pic.url_medium,
                    'url_large': pic.url_large,
                }})
            else:
                return HttpResponseRedirect(request.path)
    else:
        form = PicUploadForm()

    tpl = 'companydb/db_pics.html'
    ctx = {'form': form, 'photos': Pic.objects.all_for_profile(request.user)}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def db_projects(request, pk=None):
    """
    Provide a form to add a "project" to a company profile. A project includes
    a reference to up to 10 Stone items, a description, up to 20 pictures,
    and (in case of a pubic building) a street address, so that it can be
    visited irl.

    :param request:
    :param pk: Optionally, the pk of an existing Project.
    :return:
    """
    project = None
    if pk:
        project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = CompanyProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            redirect_url = reverse('companydb_projects')
            return HttpResponseRedirect(redirect_url)
    else:
        form = CompanyProjectForm(instance=project)

    tpl = 'companydb/db_project.html'
    ctx = {'form': form}
    return rtr(tpl, ctx, context_instance=RequestContext(request))


def db_stock(request, pk=None):

    tpl = 'companydb/db_project.html'
    ctx = {'form': form}
    return rtr(tpl, ctx, context_instance=RequestContext(request))
