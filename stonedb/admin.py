from django.contrib import admin
from .models import Stone, StoneName, Color, Country, Texture, Classification


class StoneAdmin(admin.ModelAdmin):
    ordering = ('name', )
    list_display = ('name', 'slug', 'color', 'classification', 'texture',
                    'country', )


class StoneNameAdmin(admin.ModelAdmin):
    ordering = ('name', 'stone', )
    list_display = ('stone', 'name', 'slug', )


admin.site.register(Stone, StoneAdmin)
admin.site.register(StoneName, StoneNameAdmin)

admin.site.register(Color)
admin.site.register(Country)
admin.site.register(Texture)
admin.site.register(Classification)
