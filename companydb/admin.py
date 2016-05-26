from django.contrib import admin
from django.contrib.admin import ModelAdmin

from companydb.models import Group, Pic, Project, Stock, UserProfile, Product, \
    Country, Spam


class UserProfileAdmin(ModelAdmin):
    readonly_fields = ('user', 'signup_ip', 'lastlogin_ip', )
    exclude = ('country_sub_id', 'country_old_id', 'postal', 'fax',
               'country_name', )
    view_on_site = True


class GroupAdmin(ModelAdmin):
    exclude = ('created', 'members', 'keywords', )
    readonly_fields = ('count_members', 'slug', )
    view_on_site = True


class ProductAdmin(ModelAdmin):
    exclude = ('created', 'companies', )
    readonly_fields = ('slug', )
    view_on_site = True


class CountryAdmin(ModelAdmin):
    readonly_fields = ('slug', 'geonameid', 'cc', 'phone', )
    view_on_site = True


admin.site.register(Spam)
admin.site.register(Pic)
admin.site.register(Project)
admin.site.register(Stock)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Country, CountryAdmin)
