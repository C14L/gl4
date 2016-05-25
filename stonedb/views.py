from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods

from companydb.models import Stock, Project, Pic
from stonedb.forms import StoneSearchByNameForm
from stonedb.models import Stone, Classification, Color, Country, Texture, \
    StoneName
from toolbox import force_int

FILTER_URL_NO_VALUE = 'all'
STONES_PER_PAGE = getattr(settings, 'STONES_PER_PAGE', 50)


def _get_page(o, p, pp=None):
    paginator = Paginator(o, pp or getattr(settings, 'STONES_PER_PAGE', 100))
    try:
        page = paginator.page(p)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        raise Http404
    return page


def _ctx(ctx):
    ctx['tpl_search_form'] = 'stones'
    return ctx


def home(request):
    return render(request, 'stonedb/home.html', _ctx({
        'form': StoneSearchByNameForm(),
        'classifications': Classification.objects.all_with_stones(),
        'colors': Color.objects.all_with_stones(),
        'countries': Country.objects.all_with_stones(),
        'textures': Texture.objects.all_with_stones(), }))


@require_http_methods(["GET"])
def redir_search_php(request):
    # /stone/redir_search.php?p=1&color=&country=&classification=13&pseu=
    #  -->
    # /stone/france/coarse-grained/blue/sandstone
    p = force_int(request.GET.get('p', 1))
    color = force_int(request.GET.get('color', 0))
    country = force_int(request.GET.get('country', 0))
    texture = force_int(request.GET.get('texture', 0))
    classification = force_int(request.GET.get('type', 0))

    if color:
        color = get_object_or_404(Color, pk=color)
    if country:
        country = get_object_or_404(Country, pk=country)
    if texture:
        texture = get_object_or_404(Texture, pk=texture)
    if classification:
        classification = get_object_or_404(Classification, pk=classification)

    # Now redirect depending on what values we received.
    if not (color or country or texture or classification):
        # no vals at all?!
        url = reverse('stonedb_home')
    elif color and not (country or texture or classification):
        # only color
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'color', 'q': color.slug})
    elif country and not (color or texture or classification):
        # only country
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'country', 'q': country.slug})
    elif texture and not (color or country or classification):
        # only texture
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'texture', 'q': texture.slug})
    elif classification and not (color or country or texture):
        # only classification
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'type', 'q': classification.slug})
    else:
        # if there are at least two properties defined, then show filter page.
        url = reverse('stonedb_filter', kwargs={
            'color': getattr(color, 'slug', FILTER_URL_NO_VALUE),
            'country': getattr(country, 'slug', FILTER_URL_NO_VALUE),
            'texture': getattr(texture, 'slug', FILTER_URL_NO_VALUE),
            'classif': getattr(classification, 'slug', FILTER_URL_NO_VALUE)})
        if p > 1:
            url['p'] = p

    return HttpResponsePermanentRedirect(url)


def property_list(request, f):
    """
    Simple links page with links to all "colors" or all "countries".

    :type request: object
    :type f: str 'color', 'country', 'type', 'texture'
    """
    f = f.lower()
    fk = f

    if f == 'color':
        li = Color.objects.all_with_stones()
    elif f == 'country':
        li = Country.objects.all_with_stones()
    elif f == 'texture':
        li = Texture.objects.all_with_stones()
    elif f in ['type', 'classification']:
        li = Classification.objects.all_with_stones()
        fk = 'classification'
    else:
        raise Http404

    ctx = {'items': li, 'f': f, 'fk': fk}
    return render(request, 'stonedb/property_list.html', _ctx(ctx))


def simple_filter(request, f, q, p=None):
    """Return a list of stones for one filter, e.g. color.

    :type f: str -> filter (color, country, type)
    :type q: str -> query (color name, etc.)
    :type p: int -> page number (always None for page 1)

    Example: /stone/color/blue/
    """
    if p == '1':
        # Don't show page 1 number in URL. Example: /stone/color/blue/1
        return HttpResponsePermanentRedirect(request.path[:-2])

    p = p or 1  # no page number means page 1
    f = f.lower()
    fk = f  # filter "type" needs "classification" as filter key

    if f == 'color':
        more = Color.objects.all_with_stones()
        q = get_object_or_404(Color, slug=q)
    elif f == 'country':
        more = Country.objects.all_with_stones()
        q = get_object_or_404(Country, slug=q)
    elif f == 'texture':
        more = Texture.objects.all_with_stones()
        q = get_object_or_404(Texture, slug=q)
    elif f == 'type':
        more = Classification.objects.all_with_stones()
        fk = 'classification'
        q = get_object_or_404(Classification, slug=q)
    else:
        raise Http404

    titlestone = '/stonesbrowse/{}.jpg'.format(q.slug)

    stones = _get_page(Stone.objects.filter(**{fk: q}), p, 60)
    return render(request, 'stonedb/filter_{}.html'.format(fk), _ctx({
        'range_pages': range(1, stones.paginator.num_pages+1),
        'canonical': request.path,
        'titlestone': titlestone,
        'stones': stones,
        'more': more,
        'f': f,
        'q': q,
        fk: q,
        'selected_{}'.format(fk): q.pk
    }))


def _filter_cleanup_val(k):
    k = k.lower()
    if k == FILTER_URL_NO_VALUE:
        k = ''
    return k


def filter(request, color, country, texture, classif, p=1):
    """Return a list of stones for a specific color+type+origin.

    Exampe: /stone/sandstone/blue/veined/france/
    :param request:
    :param color:
    :param country:
    :param texture:
    :param classif:
    :param p:
    """
    if p == '1':
        # Don't show page 1 number in URL.
        # Example: /stone/sandstone/blue/veined/france/1
        return HttpResponsePermanentRedirect(request.path[:-2])

    p = force_int(p) or 1
    url = ''
    color = _filter_cleanup_val(color)
    country = _filter_cleanup_val(country)
    texture = _filter_cleanup_val(texture)
    classif = _filter_cleanup_val(classif)

    # Now redirect depending on what values we received.
    if not (color or country or texture or classif):
        # no vals at all is not possible, go to redir_search page.
        url = reverse('stonedb_home')
    elif color and not (country or texture or classif):
        # only color, go to old color page
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'color', 'q': color.slug})
    elif country and not (color or texture or classif):
        # only country, go to old country page.
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'country', 'q': country.slug})
    elif texture and not (color or country or classif):
        # only texture, there is NO old texture page, so that's okay.
        pass
    elif classif and not (color or country or texture):
        # only classification, go to old "type" page.
        url = reverse('stonedb_simple_filter',
                      kwargs={'f': 'classif', 'q': classif.slug})

    if url:
        return HttpResponsePermanentRedirect(url)

    # Still here? Then display the filtered results.
    li = Stone.objects.all()

    if color:
        color = get_object_or_404(Color, slug=color)
        li = li.filter(color=color)
    if country:
        country = get_object_or_404(Country, slug=country)
        li = li.filter(country=country)
    if texture:
        texture = get_object_or_404(Texture, slug=texture)
        li = li.filter(texture=texture)
    if classif:
        classif = get_object_or_404(Classification, slug=classif)
        li = li.filter(classification=classif)

    # Canonical is the URI with NO page number
    stones = _get_page(li, p, 60)
    canonical = reverse('stonedb_filter', args=[
                        country and country.slug or 'all',
                        texture and texture.slug or 'all',
                        color and color.slug or 'all',
                        classif and classif.slug or 'all'])

    titlestone = '/stonesbrowse/{}.jpg'.format('-'.join([x for x in [
        country and country.slug, texture and texture.slug,
        color and color.slug, classif and classif.slug] if x]))

    return render(request, 'stonedb/filter.html', _ctx({
        'range_pages': range(1, stones.paginator.num_pages+1),
        'canonical': canonical,
        'titlestone': titlestone,
        'stones': stones,
        'classification': classif,
        'color': color,
        'country': country,
        'texture': texture,
        'selected_classification': getattr(classif, 'id', ''),
        'selected_color': getattr(color, 'id', ''),
        'selected_country': getattr(country, 'id', ''),
        'selected_texture': getattr(texture, 'id', '')}))


def item(request, q):
    """Return data page for one stone."""
    stone = Stone.objects.filter(slug=q).first()
    if not stone:
        raise Http404
    stocks = Stock.objects.all_for_stone(stone)
    projects = Project.objects.all_for_stone(stone)
    pics = Pic.objects.all_for_stone(stone)

    return render(request, 'stonedb/item.html', _ctx({
        'stone': stone,
        'classification': stone.classification,
        'color': stone.color,
        'country': stone.country,
        'texture': stone.texture,
        'pics': pics,
        'projects': projects,
        'stocks': stocks,
        'canonical': reverse('stonedb_item', args=[stone.slug]),
        'selected_classification': getattr(stone.classification, 'id', ''),
        'selected_color': getattr(stone.color, 'id', ''),
        'selected_country': getattr(stone.country, 'id', ''),
        'selected_texture': getattr(stone.texture, 'id', '')}))


def api_search(request):
    """
    Search stones by name for the autocomplete input box.

    :param request: HttpRequest
    :return: JsonResponse
    """
    li, limit = [], 100
    q = slugify(request.GET.get('q', ''))  # query string
    if len(q) < 3:
        return JsonResponse({'items': []})

    def get_obj(x):
        return {'id': x.stone.id, 'pseu': x.name, 'name': x.stone.name,
                'slug': x.stone.slug, 'pic': x.stone.get_pic_thumb(),
                'url': reverse('stonedb_item', args=[x.stone.slug])}

    def add_all(qs):
        for a in qs:
            if a.id not in [b['id'] for b in li]:
                li.append(get_obj(a))

    # First find stones that have a name that begins with redir_search query.
    add_all(StoneName.objects.filter(slug__startswith=q)
            .distinct('stone__name').order_by('stone__name')
            .prefetch_related('stone')[:limit])

    # If there are few results, then also find stones that have the redir_search
    # query somewhere in their names.
    if len(li) < limit:
        add_all(StoneName.objects.filter(slug__contains=q)
                .exclude(slug__startswith=q)
                .distinct('stone__name').order_by('stone__name')
                .prefetch_related('stone')[:limit])

    return JsonResponse({'items': sorted(li, key=lambda x: x['name'])[:limit]})
