from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from markdown import markdown


class Keyword(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Keyword, self).save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    about = models.TextField(default='', blank=True)
    url = models.URLField(default='', blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super(Author, self).save(*args, **kwargs)


class Topic(models.Model):
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField()
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super(Topic, self).save(*args, **kwargs)


class ArticleManager(models.Manager):

    def published(self):
        return self.filter(is_published=True)\
                   .prefetch_related('topic', 'author')

    def frontpage(self):
        return self.published().filter(is_frontpage=True)

    def topic(self, topic):
        return self.published().filter(topic=topic)


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(default=now)
    user = models.ForeignKey(User)
    author = models.ForeignKey(Author, blank=True, null=True, default=None)
    keywords = models.ManyToManyField(Keyword)
    is_published = models.BooleanField(default=False)
    is_stickied = models.BooleanField(default=False)
    is_frontpage = models.BooleanField(default=False)
    topic = models.ForeignKey(Topic, blank=True, null=True, default=None)
    teaser = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    text = models.TextField(default='', blank=True)

    objects = ArticleManager()

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super(Article, self).save(*args, **kwargs)

    def keywords_str(self):
        return ', '.join(self.keywords.all())

    @property
    def html(self):
        # converts markdown text into html
        return mark_safe(markdown(self.text))

