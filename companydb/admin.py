from django.contrib import admin
from django.utils.html import format_html

from companydb.models import Group, Pic, Project, Stock, UserProfile, Product, \
    Country, Spam


admin.site.register(Spam)
admin.site.register(Pic)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'geonameid', 'cc', 'phone', )
    view_on_site = True


@admin.register(Group)  # business areas
class GroupAdmin(admin.ModelAdmin):
    exclude = ('created', 'members', 'keywords', )
    readonly_fields = ('count_members', 'slug', )
    view_on_site = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('created', 'companies', )
    readonly_fields = ('slug', )
    view_on_site = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = (('is_blocked', 'is_deleted', 'is_recommended'),
              ('user', 'created', 'count_views'),
              'stones', 'description', )
    filter_horizontal = ('stones', )
    list_display = ('pk', 'ln_stones', 'ln_user', 'created',
                    'is_blocked', 'is_public')
    list_display_links = ('pk', 'created', )
    list_editable = ('is_blocked', )
    list_filter = (('user', admin.RelatedOnlyFieldListFilter), )
    preserve_filters = True
    readonly_fields = ('user', 'created', 'count_views', )

    def ln_user(self, obj):
        s = '<a href="{}">{}</a>'
        return format_html(s.format(obj.user.profile.get_admin_url(), obj.user))

    def ln_stones(self, obj):
        s = '<a href="{}">{}</a>'
        l = [s.format(x.get_admin_url(), x.name) for x in obj.get_stones_list()]
        return format_html(', '.join(l))


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = (('is_blocked', 'is_deleted', 'is_recommended'),
              ('user', 'created', 'count_views'),
              ('dim_type', 'dim_total'),
              'stone', 'description', )
    list_display = ('pk', 'stone', 'user', 'created', 'is_public')
    list_filter = (('user', admin.RelatedOnlyFieldListFilter), )
    readonly_fields = ('user', 'created', 'count_views', )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'signup_ip', 'lastlogin_ip', )
    exclude = ('country_sub_id', 'country_old_id', 'postal', 'fax',
               'country_name', )
    view_on_site = True
