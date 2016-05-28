from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from django.utils.html import format_html

from companydb.models import Group, Pic, Project, Stock, UserProfile, Product, \
    Country, Spam


admin.site.register(Spam)
admin.site.register(Pic)


class ByCompanyListFilter(SimpleListFilter):
    """Filter lists company names. The related list model must have a `user`
    property that is a ForeignKey to User."""
    title = 'Companies'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        qs = model_admin.model.objects.all().distinct()
        users = User.objects.filter(id__in=qs.values_list('user_id', flat=True))
        users = users.select_related('profile').order_by('profile__name')
        return [(u.id, u.profile.name) for u in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id__exact=self.value())
        else:
            return queryset


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
              ('user', 'created', 'count_views'), 'stones', 'description', )
    filter_horizontal = ('stones', )
    list_display = ('pk', 'ln_stones', 'ln_user', 'created',
                    'is_blocked', 'is_public')
    list_display_links = ('pk', 'created', )
    list_editable = ('is_blocked', )
    list_filter = (ByCompanyListFilter, )
    preserve_filters = True
    readonly_fields = ('user', 'created', 'count_views', )
    save_on_top = True

    def ln_user(self, obj):
        s = '<a href="{}">{}</a>'
        return format_html(s.format(obj.user.profile.get_admin_url(),
                                    obj.user.profile.name[:35]))

    def ln_stones(self, obj):
        s = '<a href="{}">{}</a>'
        l = [s.format(x.get_admin_url(), x.name) for x in obj.get_stones_list()]
        return format_html(', '.join(l))


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = (('is_blocked', 'is_deleted', 'is_recommended'),
              ('user', 'created', 'count_views'),
              ('dim_type', 'dim_total'), 'stone', 'description', )
    list_display = ('pk', 'ln_stone', 'ln_user', 'created',
                    'is_blocked', 'is_public')
    list_display_links = ('pk', 'created', )
    list_editable = ('is_blocked', )
    list_filter = (ByCompanyListFilter, )
    preserve_filters = True
    readonly_fields = ('user', 'created', 'count_views', )
    save_on_top = True

    def ln_user(self, obj):
        s = '<a href="{}">{}</a>'
        return format_html(s.format(obj.user.profile.get_admin_url(),
                                    obj.user.profile.name[:35]))

    def ln_stone(self, obj):
        s = '<a href="{}">{}</a>'
        return format_html(s.format(obj.stone.get_admin_url(), obj.stone.name))


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('country_sub_id', 'country_old_id', 'postal', 'fax',
               'country_name', )
    list_display = ('pk', 'name', 'user_email',
                    'city', 'country', 'is_blocked', 'is_deleted')
    list_display_links = ('pk', 'name')
    list_editable = ('is_blocked', )
    list_filter = (('country', admin.RelatedOnlyFieldListFilter), )
    list_select_related = ('user', )
    ordering = ('name', )
    preserve_filters = True
    readonly_fields = ('user', 'signup_ip', 'lastlogin_ip', )
    search_fields = ['user__email', 'name', ]
    view_on_site = True

    def user_email(self, obj):
        return obj.user.email
        # s = '<a href="{}">{}</a>'
        # return format_html(s.format(obj.user.get_admin_url(),
        #                             obj.user.email))
