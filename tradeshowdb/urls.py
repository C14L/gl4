from django.conf.urls import url
from . import views

urlpatterns = [
    # /tradeshows
    url(r'^$',
        views.home, name='tradeshowdb_home'),
    # /tradeshows/2016
    url(r'^(?P<y>[12][0-9]{3})$',
        views.by_year, name='tradeshowdb_by_year'),
    # /tradeshows/2015/construction-architecture
    url(r'^(?P<y>[12][0-9]{3})/(?P<slug>[a-zA-Z0-9_-]{1,100})$',
        views.item, name='tradeshowdb_item'),
]
