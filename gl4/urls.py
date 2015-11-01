from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import companydb.urls
import gl4app.urls
import stonedb.urls
import tradeshowdb.urls

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^company/', include(companydb.urls)),
    url(r'^stone/', include(stonedb.urls)),
    url(r'^tradeshows/', include(tradeshowdb.urls)),

    url(r'^', include(gl4app.urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    # from django.conf.urls.static import static
    # urlpatterns += static('/pics/', document_root=settings.MEDIA_ROOT)
    # urlpatterns += static('/thumbs/', document_root=settings.MEDIA_ROOT)
