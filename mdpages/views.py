from django.shortcuts import render_to_response as rtr
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from mdpages.models import Article, Author, Keyword, Topic


def home_view(request, template_name='mdpages/home.html'):
    # list featured articles and all topics
    topics = Topic.objects.all()
    authors = Author.objects.all()[:10]
    articles = Article.objects.filter(is_published=True, is_frontpage=True)
    ctx = {'topics': topics, 'authors': authors, 'articles': articles}
    return rtr(template_name, ctx, context_instance=RequestContext(request))


def topic_view(request, topic, template_name='mdpages/topic.html'):
    # one topic with a list of related articles
    topic = get_object_or_404(Topic, slug=topic)
    articles = Article.objects.filter(topic=topic, is_published=True)
    ctx = {'topic': topic, 'articles': articles}
    return rtr(template_name, ctx, context_instance=RequestContext(request))


def article_view(request, topic, article, template_name='mdpages/article.html'):
    # show one article
    topic = get_object_or_404(Topic, slug=topic)
    article = get_object_or_404(Article,
                                topic=topic, slug=article, is_published=True)
    ctx = {'article': article, 'topic': topic}
    return rtr(template_name, ctx, context_instance=RequestContext(request))


def author_view(request, author, template_name='mdpages/author.html'):
    # show one author info page
    author = get_object_or_404(Author, slug=author)
    ctx = {'author': author}
    return rtr(template_name, ctx, context_instance=RequestContext(request))


def keyword_view(request, keyword, template_name='mdpages/keyword.html'):
    # list all articles that belong to the keyword
    keyword = get_object_or_404(Keyword, slug=keyword)
    ctx = {'keyword': keyword}
    return rtr(template_name, ctx, context_instance=RequestContext(request))
