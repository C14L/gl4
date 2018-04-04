from django.conf import settings
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from mdpages.models import Article, Author, Keyword, Topic


def home_view(request):
    """List featured articles and all topics."""
    p = request.GET.get('p', 1)
    per_page = getattr(settings, 'MDPAGES_PER_PAGE', 10)
    topics = Topic.objects.all()
    authors = Author.objects.all()[:10]
    articles = Paginator(Article.objects.frontpage(), per_page)
    return render(request, 'mdpages/home.html', {
        'topics': topics, 'authors': authors, 'articles': articles.page(p),
        'canonical': reverse('mdpages_home')})


def topic_view(request, topic):
    """One topic with a list of related articles."""
    p = request.GET.get('p', 1)
    per_page = getattr(settings, 'MDPAGES_PER_PAGE', 10)
    topic = get_object_or_404(Topic, slug=topic)
    articles = Paginator(Article.objects.topic(topic), per_page)
    return render(request, 'mdpages/topic.html', {
        'canonical': reverse('mdpages_topic', args=[topic.slug]),
        'topic': topic, 'articles': articles.page(p)})


def article_view(request, topic, article):
    """Show one article."""
    topic = get_object_or_404(Topic, slug=topic)
    article = get_object_or_404(
        Article, topic=topic, slug=article, is_published=True)
    kwargs = {'topic': topic.slug, 'article': article.slug}
    canonical = reverse('mdpages_article', kwargs=kwargs)
    return render(request, 'mdpages/article.html', {
        'article': article, 'topic': topic, 'canonical': canonical})


def author_view(request, author):
    """Show one author info page."""
    author = get_object_or_404(Author, slug=author)
    return render(request, 'mdpages/author.html', {'author': author})


def keyword_view(request, keyword):
    """List all articles that belong to the keyword."""
    keyword = get_object_or_404(Keyword, slug=keyword)
    return render(request, 'mdpages/keyword.html', {'keyword': keyword})
