from os.path import join

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import gl4app.views
import companydb.views
import stonedb.views
import tradeshowdb.views


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^infos/', include('mdpages.urls')),

    # gl4app
    url(r'^$', gl4app.views.home, name='home'),

    # stonedb
    url(r'^stone$',
        stonedb.views.home, name='stonedb_home'),

    # /stone/search.php --> stonedb_filter
    url(r'^stone/search.php$',
        stonedb.views.redir_search_php, name='stonedb_redir_search_php'),

    # /stone/color
    # /stone/type
    url(r'^stone'
        r'/(?P<f>color|country|type|texture)$',
        stonedb.views.property_list, name='stonedb_property_list'),

    # /stone/color/blue
    # /stone/country/france/3
    # /stone/type/sandstone
    url(r'^stone'
        r'/(?P<f>color|country|type|texture)'
        r'/(?P<q>[a-zA-Z0-9_-]{1,100})'
        r'(?:/(?P<p>\d{1,3}))?$',
        stonedb.views.simple_filter, name='stonedb_simple_filter'),

    # /stone/aachener-blaustein
    # /stone/aachener-blaustein/comments
    # /stone/aachener-blaustein/pictures
    url(r'^stone/'
        r'(?P<q>[a-zA-Z0-9_-]{1,100})$',
        stonedb.views.item, name='stonedb_item'),

    # /stone/france/coarse-grained/blue/sandstone
    url(r'^stone'
        r'/(?P<country>[a-zA-Z0-9_-]{1,30})'
        r'/(?P<texture>[a-zA-Z0-9_-]{1,30})'
        r'/(?P<color>[a-zA-Z0-9_-]{1,30})'
        r'/(?P<classif>[a-zA-Z0-9_-]{1,30})'
        r'(?:/(?P<p>[2-9]))?$',
        stonedb.views.filter, name='stonedb_filter'),

    url(r'api/search/stones/',
        stonedb.views.api_search, name='stonedb_api_search'),

    # tradeshowdb

    url(r'^tradeshows/?$',
        tradeshowdb.views.home, name='tradeshowdb_home'),
    # /tradeshows/2016
    url(r'^tradeshows/(?P<y>[12][0-9]{3})$',
        tradeshowdb.views.home, name='tradeshowdb_by_year'),
    # /tradeshows/2015/construction-architecture
    url(r'^tradeshows/(?P<y>[12][0-9]{3})/(?P<slug>[a-zA-Z0-9_-]{1,100})$',
        tradeshowdb.views.item, name='tradeshowdb_item'),

    # companydb: /companies
    url(r'^companies$', companydb.views.home, name='companydb_home'),
    # /companies/memorials-grave-stones/1
    url(r'^companies/(?P<slug>[a-zA-Z0-9_-]{1,30})/(?P<p>[1-9][0-9]*)$',
        companydb.views.itemlist, name='companydb_list'),

    # /company/xxxxxxxxxx
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})$',
        companydb.views.item, name='companydb_item'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/delete$',
        companydb.views.delete, name='companydb_delete'),

    # /company/xxxxxxxxxx/stock
    #
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/stock$',
        companydb.views.stock, name='companydb_stock'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/stock/(?P<pk>\d+)$',
        companydb.views.stock_detail, name='companydb_stock_detail'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/stock/new$',
        companydb.views.stock_detail, name='companydb_stock_detail_new'),

    # /company/xxxxxxxxxx/projects
    #
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/projects$',
        companydb.views.projects, name='companydb_projects'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/projects/(?P<pk>\d+)$',
        companydb.views.projects_detail, name='companydb_projects_detail'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/projects/new$',
        companydb.views.projects_detail, name='companydb_projects_detail_new'),

    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/details/$',
        companydb.views.db_details, name='companydb_details'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/about/$',
        companydb.views.db_about, name='companydb_about'),
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/business-areas/$',
        companydb.views.db_areas, name='companydb_areas'),

    # /company/xxxxxxxxxx/contact
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/contact$',
        companydb.views.contact, name='companydb_contact'),
    # /company/xxxxxxxxxx/photos
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/photos$',
        companydb.views.photos, name='companydb_photos'),

    # REDIR /company/xxxxxxxxxx/photos/12345 --> /fotos/12345
    url(r'^company/(?P<slug>[a-zA-Z0-9_-]{1,30})/photos/(?P<id>\d+)$',
        companydb.views.photo_redir, name='companydb_photo_redir'),
    # /fotos/12345
    url(r'^fotos/(?P<id>\d+)$',
        companydb.views.pic_item, name='companydb_pic_item'),

    # url(r'^company/dashboard/$',
    #     companydb.views.dashboard, name='companydb_dashboard'),
    # url(r'^company/-/projects/$',
    #     companydb.views.projects_detail, name='companydb_db_projects'),
    # url(r'^company/-/stock/$',
    #     companydb.views.stock_detail, name='companydb_db_stock'),
]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^rosetta/', include('rosetta.urls')), ]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static('/stonesindex/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonesindex'))

    urlpatterns += static('/stonespics/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonespics'))

    urlpatterns += static('/api_static/', document_root=join(
        settings.BASE_DIR, 'api_static'))

    # urlpatterns += static('/stonespics/', document_root=settings.MEDIA_ROOT)
    # static files (images, css, javascript, etc.)
