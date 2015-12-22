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
        r'(?:/(?P<p>[2-9]))?$',
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

    # tradeshowdb
    url(r'^tradeshows$',
        tradeshowdb.views.home, name='tradeshowdb_home'),
    # /tradeshows/2016
    url(r'^tradeshows/(?P<y>[12][0-9]{3})$',
        tradeshowdb.views.home, name='tradeshowdb_by_year'),
    # /tradeshows/2015/construction-architecture
    url(r'^tradeshows/(?P<y>[12][0-9]{3})/(?P<slug>[a-zA-Z0-9_-]{1,100})$',
        tradeshowdb.views.item, name='tradeshowdb_item'),

    # companydb
    url(r'^company$', companydb.views.home, name='companydb_home'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    from django.conf.urls.static import static
    urlpatterns += static('/stonesindex/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonesindex'))
    urlpatterns += static('/stonespics/', document_root=join(
        settings.BASE_DIR, 'stonedb/stonesimages/stonespics'))

    # urlpatterns += static('/stonespics/', document_root=settings.MEDIA_ROOT)
