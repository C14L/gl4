from django.conf.urls import url
from mdpages import views

urlpatterns = [
    url(r'^$',
        views.home_view, name='mdpages_home'),
    url(r'^author/(?P<author>[a-z0-9_-]+)/?$',
        views.author_view, name='mdpages_author'),
    url(r'^tag/(?P<author>[a-z0-9_-]+)/?$',
        views.keyword_view, name='mdpages_keyword'),
    url(r'^(?P<topic>[a-z0-9_-]+)/?$',
        views.topic_view, name='mdpages_topic'),
    url(r'^(?P<topic>[a-z0-9_-]+)/(?P<article>[a-z0-9_-]+)/?$',
        views.article_view, name='mdpages_article'),
]
