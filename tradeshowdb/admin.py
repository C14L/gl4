from django.contrib import admin
from tradeshowdb.models import Tradeshow


class TradeshowAdmin(admin.ModelAdmin):
    ordering = ('begins', 'name', )
    list_display = ('aumaid', 'name', 'begins', 'ends',
                    'city_name', 'country_name', )


admin.site.register(Tradeshow, TradeshowAdmin)
