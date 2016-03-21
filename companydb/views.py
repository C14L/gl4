from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, \
    HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response as rtr
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from companydb.forms import PicUploadForm, CompanyDetailsForm, \
    CompanyAboutForm, CompanyProjectForm, CompanyStockForm
from companydb.models import Group, Pic, Stock, Project
from mdpages.models import Article
from stonedb.models import Stone


def _get_page(o, p):
    per_page = getattr(settings, 'PER_PAGE', 20)
    paginator = Paginator(o, per_page)
    return paginator.page(p)


def home(request):
    ctx = {'groups': Group.objects.all()}
    return render(request, 'companydb/home.html', ctx)


def itemlist(request, slug, p):
    group = get_object_or_404(Group, slug=slug)
    members_qs = group.members.filter(is_active=True,
                                      profile__is_deleted=False,
                                      profile__is_blocked=False)
    members_qs = members_qs.prefetch_related('profile')
    members_qs = members_qs.order_by('profile__name')
    members = _get_page(members_qs, p)

    ctx = {'group': group, 'members': members,
           'range_pages': range(1, members.paginator.num_pages+1)}
    return render(request, 'companydb/list.html', ctx)


def item(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    pics = Pic.objects.filter(user=view_user, module='profile')
    ctx = {'view_user': view_user, 'pics': pics}
    return render(request, 'companydb/item.html', ctx)


def stock(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = view_user.stock_set.filter(is_deleted=False, is_blocked=False)
    ctx = {'view_user': view_user, 'stock': _get_page(li, page)}
    return render(request, 'companydb/stock.html', ctx)


@login_required
def stock_detail(request, pk=None):
    if pk:
        view_item = get_object_or_404(Stock, pk=pk)
    else:
        view_item = None

    if request.method == 'POST':
        form = CompanyStockForm(request.POST, instance=view_item)
        # manually add stone selected
        stone_pk = request.POST.get('stone', None)
        stone = get_object_or_404(Stone, pk=stone_pk)
        # manually add uploaded pics selection
        pics_pks = request.POST.getlist('pics', [])
        print('pics_pks: ', pics_pks)
        pics = Pic.objects.all_for_user(request.user) \
                          .filter(pk__in=pics_pks, module='stock')
        print('pics: ', pics)

        if form.is_valid():
            stock_item = form.save(commit=False)
            stock_item.stone = stone
            stock_item.user = request.user
            stock_item.save()

            # point pictures to the new Stone item
            for p in pics:
                print('SAVING PIC: ', dir(p))
                p.attach_to(stock_item.id)

            redirect_url = reverse('companydb_db_stock_item',
                                   kwargs={'pk': stock_item.id})
            return HttpResponseRedirect(redirect_url)
    else:
        form = CompanyStockForm(instance=view_item)

    li = request.user.stock_set.all()
    ctx = {'form': form, 'stocklist': li, 'stockitem': view_item}
    return render(request, 'companydb/stock_detail.html', ctx)


def projects(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = view_user.project_set.filter(is_deleted=False, is_blocked=False)
    ctx = {'view_user': view_user, 'projects': _get_page(li, page)}
    return render(request, 'companydb/projects.html', ctx)


@login_required
@require_http_methods(["POST", "GET", "HEAD", "DELETE"])
def projects_detail(request, pk=None):
    """
    Provide a form to add a "project" to a company profile. A project includes
    a reference to up to 10 Stone items, a description, up to 20 pictures,
    and (in case of a pubic building) a street address, so that it can be
    visited irl.
    """

    if pk:
        view_item = get_object_or_404(Project, user=request.user, pk=pk)
    else:
        view_item = None

    if 'DELETE' in (request.method, request.POST.get('_method', None)):
        # This deletes the entire view_item and and all attached pics.
        view_item.delete()
        kwargs = {'slug': request.user.username}
        redirect_url = reverse('companydb_projects', kwargs=kwargs)
        return HttpResponseRedirect(redirect_url)

    if 'POST' == request.method:
        form = CompanyProjectForm(request.POST, instance=view_item)
        # manually add stones selection
        stone_pks = request.POST.getlist('stones', [])
        stones = Stone.objects.filter(pk__in=stone_pks)
        # manually add uploaded pics selection
        pics_pks = request.POST.getlist('pics', [])
        pics = Pic.objects.all_for_user(request.user) \
                          .filter(pk__in=pics_pks, module='projects')

        if form.is_valid():
            project_item = form.save(commit=False)
            project_item.user = request.user
            project_item.save()
            print('--> projects_detail -> project_item saved.')
            print(project_item)

            print('--> projects_detail -> adding stones to project_item...')
            project_item.stones = stones
            print('--> projects_detail -> saving project_item again...')
            project_item.save()

            # point pictures to the new Project item
            for p in pics:
                p.attach_to(project_item.pk)

            redirect_url = request.POST.get('next', reverse(
                'companydb_db_projects_item', kwargs={'pk': project_item.id}))
            return HttpResponseRedirect(redirect_url)
    else:
        form = CompanyProjectForm(instance=view_item)

    li = request.user.project_set.all()
    ctx = {'form': form, 'projects': li, 'project': view_item}
    return render(request, 'companydb/projects_detail.html', ctx)


def photos(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = Pic.objects.all_for_profile(view_user)
    form = PicUploadForm() if request.user == view_user else None

    ctx = {'view_user': view_user, 'form': form, 'photos': _get_page(li, page)}
    return render(request, 'companydb/photos.html', ctx)


@login_required
def db_pics(request):

    if request.method == 'POST':
        module = request.POST.get('module', 'profile')
        if module not in [x[0] for x in Pic.MODULE_CHOICES]:
            raise ValueError('Module does not exist.')

        form = PicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print('--> db_pics() --> FORM VALID')
            if module == 'profile':
                pic = Pic.objects.add_to_profile(request.user,
                                                 request.FILES['pic'],
                                                 form.cleaned_data['title'])
            else:
                pic = Pic.objects.add_upload(request.user,
                                             request.FILES['pic'], module)

            if request.is_ajax():
                print('--> db_pics() --> REQUEST AJAX')
                return JsonResponse({'pic': {
                    'id': pic.id,
                    'url': reverse('companydb_pic_item', kwargs={'id': pic.id}),
                    'url_thumb': pic.url_thumb,
                    'url_small': pic.url_small,
                    'url_medium': pic.url_medium,
                    'url_large': pic.url_large,
                }})
            else:
                print('--> db_pics() --> REQUEST HTML')
                return HttpResponseRedirect(request.path)
    else:
        # form = PicUploadForm()
        kwargs = {'slug': request.user.username}
        _next = reverse('companydb_photos', kwargs=kwargs)
        return HttpResponseRedirect(_next)

    ctx = {'form': form, 'photos': Pic.objects.all_for_profile(request.user)}
    return render(request, 'companydb/pics_detail.html', ctx)


def contact(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    return render(request, 'companydb/contact.html', {'view_user': view_user})


def photo_redir(request, slug, id):
    pic = get_object_or_404(Pic, pk=id)
    _next = reverse('companydb_pic_item', kwargs={'id': pic.id})
    return HttpResponsePermanentRedirect(_next)


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

    if request.user.is_authenticated() and request.user.id == pic.user.id:
        if 'DELETE' in (request.method, request.POST.get('_method', None)):
            pic.delete()
            _next = request.POST.get('next', reverse('companydb_db_pics'))
            return HttpResponseRedirect(_next)

    if request.is_ajax():
        print('--> pic_item() --> REQUEST AJAX')
        return JsonResponse({'pic': pic})

    ctx = {'pic': pic, 'related': related, 'view_user': pic.user}
    return render(request, 'companydb/pic_item.html', ctx)


@login_required
def dashboard(request):
    return render(request, 'companydb/dashboard.html')


@login_required
def db_details(request):
    if request.method == 'POST':
        form = CompanyDetailsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            _next = reverse('companydb_item', args=[request.user.username])
            return HttpResponseRedirect(_next)
    else:
        form = CompanyDetailsForm(instance=request.user.profile)

    return render(request, 'companydb/db_details.html', {'form': form})


def db_about(request):
    if request.method == 'POST':
        form = CompanyAboutForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            _next = reverse('companydb_item', args=[request.user.username])
            return HttpResponseRedirect(_next)
    else:
        form = CompanyAboutForm(instance=request.user.profile)

    return render(request, 'companydb/db_about.html', {'form': form})


@login_required
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

    ctx = {'groups': Group.objects.all()}
    return render(request, 'companydb/db_areas.html', ctx)





