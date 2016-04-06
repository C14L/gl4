from django.contrib import admin
from mdpages.models import Article, Author, Keyword, Topic


class ArticleAdmin(admin.ModelAdmin):
    # save_on_top = True
    list_display = ('title', 'topic', 'created',)
    list_per_page = 50
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

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Topic)
