from django.contrib import admin
from tradeshowdb.models import Tradeshow


@admin.register(Tradeshow)
class TradeshowAdmin(admin.ModelAdmin):
    date_hierarchy = 'begins'
    list_display = ('aumaid', 'name', 'begins', 'ends',
                    'city_name', 'country_name', )
    list_filter = ('country_name', )
    ordering = ('begins', 'name', )
    search_fields = ['name', ]
