from django.views.generic import RedirectView
from os.path import join

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import gl4app.views
import companydb.views
import stonedb.views
import tradeshowdb.views

"""
German language URL pattern definitions. Easier to set up here than to mix URL
paths with other translations in locale files using i18n patterns.
"""

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^aktuelles/', include('mdpages.urls')),

    url(r'contact$',
        RedirectView.as_view(url='/firmen/csx#contact'),
        name='contact'),

    # gl4app
    url(r'^$', gl4app.views.home, name='home'),
    # redirect to logged in user's profile, or to home `/`
    url(r'^u/?$', gl4app.views.user_home, name='user_home'),

    # stonedb
    url(r'^naturstein$',
        stonedb.views.home, name='stonedb_home'),

    # /stone/redir_search.php --> stonedb_filter
    url(r'^naturstein/search.php$',
        stonedb.views.redir_search_php, name='stonedb_redir_search_php'),

    # /stone/color
    # /stone/type
    url(r'^naturstein'
        r'/(?P<f>farbe|herkunftsland|steinart|textur)$',
        stonedb.views.property_list, name='stonedb_property_list'),

    # /stone/color/blue -> naturstein/steinart/basalt
    # /stone/country/france/3
    # /stone/type/sandstone
    url(r'^naturstein'
        r'/(?P<f>farbe|herkunftsland|steinart|textur)'
        r'/(?P<q>[a-zA-Z0-9_-]{1,100})'
        r'(?:/(?P<p>\d{1,3}))?$',
        stonedb.views.simple_filter, name='stonedb_simple_filter'),

    # /stone/aachener-blaustein
    url(r'^naturstein/'
        r'(?P<q>[a-zA-Z0-9_-]{1,100})$',
        stonedb.views.item, name='stonedb_item'),

    # /stone/france/coarse-grained/blue/sandstone
    url(r'^naturstein'
        r'/(?P<country>[a-zA-Z0-9_-]{1,30})'
        r'/(?P<texture>[a-zA-Z0-9_-]{1,30})'
        r'/(?P<color>[a-zA-Z0-9_-]{1,30})'
        r'/(?P<classif>[a-zA-Z0-9_-]{1,30})'
        r'(?:/(?P<p>\d))?$',
        stonedb.views.filter, name='stonedb_filter'),

    url(r'api/redir_search/stones/',
        stonedb.views.api_search, name='stonedb_api_search'),

    # tradeshowdb

    url(r'^fachmessen/?$',
        tradeshowdb.views.home, name='tradeshowdb_home'),

    # /fachmessen/2016
    url(r'^tradeshows/(?P<y>[12][0-9]{3})$',
        tradeshowdb.views.home, name='tradeshowdb_by_year'),

    # /tradeshows/2015/construction-architecture
    url(r'^fachmessen/(?P<y>[12][0-9]{3})/(?P<slug>[a-zA-Z0-9_-]{1,100})$',
        tradeshowdb.views.item, name='tradeshowdb_item'),

    # companydb: /companies

    url(r'^naturstein-betriebe$', companydb.views.home, name='companydb_home'),
    # /companies/redir_search?country=342&business=memorials-grave-stones

    url(r'^companies/redir_search$',
        companydb.views.redir_search, name='companydb_redir_search'),

    # /companies/consultancy-quality-assurance/1 <--[group]---
    url(r'^naturstein-betriebe/'
        r'(?P<slug>[a-zA-Z0-9_-]{1,30})/'
        r'(?P<p>[1-9][0-9]*)$',
        companydb.views.list_by_group, name='companydb_group'),

    # REDIRECT: /companies/kitchen-countertops/1 <--[product]---
    url(r'^naturstein-betriebe/'
        r'(?P<slug>[a-zA-Z0-9_-]{1,30})/?$',
        RedirectView.as_view(pattern_name='companydb_group'),
        {'p': 1}, name='companydb_group_redir'),

    # /companies/kitchen-countertops/1 <--[product]---
    url(r'^naturstein-produkte/'
        r'(?P<slug>[a-zA-Z0-9_-]{1,30})/'
        r'(?P<p>[1-9][0-9]*)$',
        companydb.views.list_by_product, name='companydb_product'),

    # /companies/kitchen-countertops/1 <--[country]---
    url(r'^naturstein-betriebe/'
        r'in/'
        r'(?P<slug>[a-zA-Z0-9_-]{1,30})/'
        r'(?P<p>[1-9][0-9]*)$',
        companydb.views.list_by_country, name='companydb_country'),

    # /companies/[country|all]/[business|all]/[product|all]/1
    url(r'^naturstein-betriebe/'
        r'(?P<country>[a-zA-Z0-9_-]{1,30})/'
        r'(?P<business>[a-zA-Z0-9_-]{1,30})/'
        r'(?P<product>[a-zA-Z0-9_-]{1,30})/'
        r'(?P<p>[1-9][0-9]*)$',
        companydb.views.search, name='companydb_search'),

    # /company/xxxxxxxxxx --> /firmen/xxxxxxxxxxxx
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})$',
        companydb.views.item, name='companydb_item'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/delete$',
        companydb.views.delete, name='companydb_delete'),

    # /company/xxxxxxxxxx/stock --> firmen/xxxxxxxxx/angebote
    #
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/angebote$',
        companydb.views.stock, name='companydb_stock'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/angebote/(?P<pk>\d+)$',
        companydb.views.stock_detail, name='companydb_stock_detail'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/angebote/new$',
        companydb.views.stock_detail, name='companydb_stock_detail_new'),

    # /company/xxxxxxxxxx/projects --> firmen/xxxxxxx/projekte
    #
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/projekte/?$',
        companydb.views.projects, name='companydb_projects'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/projekte/(?P<pk>\d+)$',
        companydb.views.projects_detail, name='companydb_projects_detail'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/projekte/new$',
        companydb.views.projects_detail, name='companydb_projects_detail_new'),

    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/details$',
        companydb.views.db_details, name='companydb_details'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/ueber$',
        companydb.views.db_about, name='companydb_about'),
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/branchen$',
        companydb.views.db_areas, name='companydb_areas'),

    # /company/xxxxxxxxxx/photos
    url(r'^firmen/(?P<slug>[a-zA-Z0-9_-]{1,30})/fotos$',
        companydb.views.photos, name='companydb_photos'),

    # REDIR /firmen/xxxxxxxxxx/photos/12345 --> /fotos/12345
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/photos/(?P<id>\d+)$',
        companydb.views.photo_redir, name='companydb_photo_redir'),
    # /fotos/12345
    url(r'^fotos/(?P<id>\d+)$',
        companydb.views.pic_item, name='companydb_pic_item'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls')), ]

if not settings.PRODUCTION:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static('/stonesindex/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonesindex'))

    urlpatterns += static('/stonespics/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonespics'))

    urlpatterns += static('/stonesbrowse/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonesbrowse'))

    urlpatterns += static('/api_static/', document_root=join(
        settings.BASE_DIR, 'api_static'))

    # urlpatterns += static('/stonespics/', document_root=settings.MEDIA_ROOT)
    # static files (images, css, javascript, etc.)
