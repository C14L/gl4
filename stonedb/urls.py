from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='stonedb_home'),

    # /stone/color/blue
    # /stone/country/france
    # /stone/type/sandstone
    url(r'^(?P<f>color|country|type)/(?P<q>[a-zA-Z0-9_-]{1,100})$',
        views.simple_filter, name='stonedb_simple_filter'),

    # /stone/blue-sandstone-from-france
    url(r'^(?P<q>[a-zA-Z0-9_-]{1,100})$',
        views.filter, name='stonedb_filter'),
]
