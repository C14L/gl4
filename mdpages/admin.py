from django.contrib import admin
from mdpages.models import Article, Author, Keyword, Topic


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created',)
    list_filter = ('topic', )
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'topic', 'text'),
        }),
        ('Meta data', {
            'classes': ('collapse', ),
            'fields': ('author', 'teaser', 'description'),
        }),
        ('Publishing', {
            'classes': ('collapse', ),
            'fields': ('created',
                       ('is_published', 'is_stickied', 'is_frontpage')),
        }),
    )
    ordering = ('created', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Topic)
