# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='title', editable=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=False)),
                ('is_stickied', models.BooleanField(default=False)),
                ('is_frontpage', models.BooleanField(default=False)),
                ('teaser', models.TextField(default='', blank=True)),
                ('description', models.TextField(default='', blank=True)),
                ('text', models.TextField(default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
                ('about', models.TextField(default='', blank=True)),
                ('url', models.URLField(default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='title', editable=False)),
                ('description', models.TextField(default='', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(null=True, to='mdpages.Author', default=None, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='keywords',
            field=models.ManyToManyField(to='mdpages.Keyword'),
        ),
        migrations.AddField(
            model_name='article',
            name='topic',
            field=models.ForeignKey(null=True, to='mdpages.Topic', default=None, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
