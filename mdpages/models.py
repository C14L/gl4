from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# https://pypi.python.org/pypi/django-autoslug
from autoslug import AutoSlugField
from markdown import markdown


class Keyword(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(editable=False, populate_from='name')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(editable=False, populate_from='name')
    about = models.TextField(default='', blank=True)
    url = models.URLField(default='', blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=200, blank=False)
    slug = AutoSlugField(editable=False, populate_from='title')  # --> url
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(editable=False, populate_from='title')  # <-- url
    created = models.DateTimeField(default=now)  # <-- "time": "2008-08-17 09:25:43"
    user = models.ForeignKey(User)  # <-- "user_id": "1",
    author = models.ForeignKey(Author, blank=True, null=True, default=None)
    keywords = models.ManyToManyField(Keyword)
    is_published = models.BooleanField(default=False)  # <-- "is_published": "1",
    is_stickied = models.BooleanField(default=False)
    is_frontpage = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, blank=True, null=True, default=None)  # <-- "topic_id": "2",
    teaser = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    text = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title

    def keywords_str(self):
        return ', '.join(self.keywords.all())

    @property
    def html(self):
        # converts markdown text into html
        return markdown(self.text)

