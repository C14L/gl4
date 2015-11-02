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
    url(r'^stone$', stonedb.views.home, name='stonedb_home'),
    # /stone/color/blue
    # /stone/country/france/3
    # /stone/type/sandstone
    url(r'^stone/(?P<f>color|country|type)/(?P<q>[a-zA-Z0-9_-]{1,100})'
        r'(?:/(?P<p>[2-9]))?$',
        stonedb.views.simple_filter, name='stonedb_simple_filter'),
    # /stone/aachener-blaustein
    # /stone/aachener-blaustein/comments
    # /stone/aachener-blaustein/pictures
    url(r'^stone/(?P<q>[a-zA-Z0-9_-]{1,100})$',
        stonedb.views.item, name='stonedb_item'),
    # /stone/blue-sandstone-from-france
    url(r'^stone/(?P<q>[a-zA-Z0-9_-]{1,100})$',
        stonedb.views.filter, name='stonedb_filter'),

    # tradeshowdb
    url(r'^$',
        tradeshowdb.views.home, name='tradeshowdb_home'),
    # /tradeshows/2016
    url(r'^(?P<y>[12][0-9]{3})$',
        tradeshowdb.views.by_year, name='tradeshowdb_by_year'),
    # /tradeshows/2015/construction-architecture
    url(r'^(?P<y>[12][0-9]{3})/(?P<slug>[a-zA-Z0-9_-]{1,100})$',
        tradeshowdb.views.item, name='tradeshowdb_item'),

    # companydb
    url(r'^company$', companydb.views.home, name='companydb_home'),

]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    # from django.conf.urls.static import static
    # urlpatterns += static('/pics/', document_root=settings.MEDIA_ROOT)
    # urlpatterns += static('/thumbs/', document_root=settings.MEDIA_ROOT)
