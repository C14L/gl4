from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, \
    HttpResponse, JsonResponse, Http404
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

from companydb.forms import PicUploadForm, CompanyDetailsForm, \
    CompanyAboutForm, CompanyProjectForm, CompanyStockForm, CompanyContactForm
from companydb.models import Group, Pic, Stock, Project
from mdpages.models import Article
from stonedb.models import Stone
from toolbox import get_login_url


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

    return render(request, 'companydb/list.html', {
        'group': group, 'members': members,
        'range_pages': range(1, members.paginator.num_pages+1)})


def item(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    pics = Pic.objects.filter(user=view_user, module='profile')
    form = CompanyContactForm()

    if 'POST' in (request.method, request.POST.get('_method', None)):
        form = CompanyContactForm(request.POST)
        if form.is_valid():
            recipients = [view_user.email]
            sender = settings.COMPANY_CONTACT_FROM_EMAIL
            subject = _('Message sent from you company profile on Graniteland.')
            tr_sender_name = _('Sender Name')
            tr_sender_mail = _('Sender Email')
            message = ('{}: {}\n{}: {}\n{}\n{}\n\n'.format(
                tr_sender_name, form.cleaned_data['name'],
                tr_sender_mail, form.cleaned_data['email'],
                ('-'*60), form.cleaned_data['msg']))

            send_mail(subject, message, sender, recipients)

            messages.info(request, _('Message sent.'))
            _next = reverse('companydb_item', args=[view_user.username])
            return HttpResponseRedirect(request.POST.get('next', _next))

    return render(request, 'companydb/item.html', {
        'view_user': view_user, 'pics': pics, 'contactform': form})


@login_required
def delete(request, slug):
    if slug != request.user.username:
        raise Http404
    return render(request, 'companydb/delete.html')


def stock(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = view_user.stock_set.filter(is_deleted=False, is_blocked=False)
    ctx = {'view_user': view_user, 'stock': _get_page(li, page)}
    return render(request, 'companydb/stock.html', ctx)


def stock_detail(request, slug, pk=None):
    form = None
    user = get_object_or_404(User, username=slug)
    view_item = Stock.objects.filter(user=user, pk=pk).first()
    can_edit = request.user.is_authenticated() and request.user == user

    if not can_edit:
        if request.method not in ['GET', 'HEAD', 'OPTIONS']:
            return HttpResponseBadRequest()
        if not view_item:
            return HttpResponseRedirect(get_login_url(request))

    if can_edit:
        if 'DELETE' in (request.method, request.POST.get('_method', None)):
            if not view_item:
                return HttpResponseBadRequest()

            # Delete the entire view_item and and all attached pics.
            view_item.delete()
            messages.success(request, _('The item was deleted.'))
            _next = reverse('companydb_stock', args=[user.username])
            return HttpResponseRedirect(redirect_url)

        elif 'POST' in (request.method, request.POST.get('_method', None)):
            form = CompanyStockForm(request.POST, instance=view_item)
            # manually add stone selected
            stone_pk = request.POST.get('stone', None)
            stone = Stone.objects.filter(pk=stone_pk).first()
            # manually add uploaded pics selection
            pics_pks = request.POST.getlist('pics', [])
            pics = Pic.objects.all_for_user(request.user)\
                              .filter(pk__in=pics_pks, module='stock')

            if form.is_valid():
                stock_item = form.save(commit=False)
                stock_item.stone = stone
                stock_item.user = request.user
                stock_item.save()
                # point pictures to the new Stone item
                for p in pics:
                    p.attach_to(stock_item.id)

                _next = reverse('companydb_stock', args=[user.username])
                return HttpResponseRedirect(request.POST.get('next', _next))

        else:
            # Return form with the item to edit, or empty form to add new item.
            form = CompanyStockForm(instance=view_item)

    return render(request, 'companydb/stock_detail.html', {
        'form': form, 'view_item': view_item, 'view_user': user})


def projects(request, slug):
    page = request.GET.get('page', 1)
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = view_user.project_set.filter(is_deleted=False, is_blocked=False)
    return render(request, 'companydb/projects.html', {
        'view_user': view_user, 'projects': _get_page(li, page)})


@require_http_methods(["POST", "GET", "HEAD", "DELETE"])
def projects_detail(request, slug, pk=None):
    """
    Provide a form to add a "project" to a company profile. A project includes
    a reference to up to 10 Stone items, a description, up to 20 pictures,
    and (in case of a pubic building) a street address, so that it can be
    visited irl.
    """
    form = None
    user = get_object_or_404(User, username=slug)
    view_item = Project.objects.filter(user=user, pk=pk).first()
    can_edit = request.user.is_authenticated() and request.user == user

    if not can_edit and not view_item:
        # Needs auth to see /new page.
        return HttpResponseRedirect(get_login_url(request))

    if can_edit:
        if 'DELETE' in (request.method, request.POST.get('_method', None)):
            if not view_item:
                return HttpResponseBadRequest()

            # Delete the entire view_item and and all attached pics.
            view_item.delete()
            messages.success(request, _('The item was deleted.'))
            _next = reverse('companydb_projects', args=[user.username])
            return HttpResponseRedirect(_next)

        elif 'POST' == request.method:
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
                project_item.stones = stones
                project_item.save()
                # point pictures to the new Project item
                for p in pics:
                    p.attach_to(project_item.pk)

                _next = reverse('companydb_projects', args=[user.username])
                return HttpResponseRedirect(request.POST.get('next', _next))
        else:
            form = CompanyProjectForm(instance=view_item)

    return render(request, 'companydb/projects_detail.html', {
        'form': form, 'projects': user.project_set.all(),
        'view_item': view_item, 'view_user': user})


def contact(request, slug):
    view_user = get_object_or_404(User, username=slug, is_active=True)
    return render(request, 'companydb/contact.html', {'view_user': view_user})


def photos(request, slug):
    page = request.GET.get('page', 1)
    form = None
    view_user = get_object_or_404(User, username=slug, is_active=True)
    li = Pic.objects.all_for_profile(view_user)
    can_edit = request.user.is_authenticated() and request.user == view_user

    if 'POST' in (request.method, request.POST.get('_method', None)):
        if not can_edit:
            return HttpResponseRedirect(get_login_url(request))

        module = request.POST.get('module', 'profile')
        if module not in [x[0] for x in Pic.MODULE_CHOICES]:
            raise ValueError('Module does not exist.')

        form = PicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            _pic = request.FILES['pic']
            if module == 'profile':
                _title = form.cleaned_data['title']
                pic = Pic.objects.add_to_profile(request.user, _pic, _title)
            else:
                pic = Pic.objects.add_upload(request.user, _pic, module)

            if request.is_ajax():
                return JsonResponse({'pic': {
                    'id': pic.id,
                    'url': reverse('companydb_pic_item', kwargs={'id': pic.id}),
                    'url_thumb': pic.url_thumb,
                    'url_small': pic.url_small,
                    'url_medium': pic.url_medium,
                    'url_large': pic.url_large,
                }})
            else:
                return HttpResponseRedirect(request.path)
        else:
            pass
    elif 'GET' in (request.method, ):
        if can_edit:
            form = PicUploadForm()

    _photos = _get_page(li, page)
    return render(request, 'companydb/photos.html', {
        'view_user': view_user, 'form': form, 'photos': _photos})


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
            if request.is_ajax():
                return HttpResponse()
            else:
                messages.success(request, _('The picture was deleted.'))
                _next = reverse('companydb_photos', args=[request.user.username])
                return HttpResponseRedirect(request.POST.get('next', _next))

    if request.is_ajax():
        return JsonResponse({'pic': pic})

    return render(request, 'companydb/pic_item.html', {
        'pic': pic, 'related': related, 'view_user': pic.user})


@login_required
def db_details(request, slug):
    if request.method == 'POST':
        form = CompanyDetailsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            _next = reverse('companydb_item', args=[request.user.username])
            return HttpResponseRedirect(_next)
    else:
        form = CompanyDetailsForm(instance=request.user.profile)

    return render(request, 'companydb/db_details.html', {'form': form})


@login_required
def db_about(request, slug):
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
def db_areas(request, slug):
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





