from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.urls import reverse
from django.db import models
from django.forms import CheckboxSelectMultiple, TextInput, Textarea
from django.utils.safestring import mark_safe

from .models import Stone, StoneName, Color, Country, Texture, Classification


class HorizCheckboxSelectMultiple(CheckboxSelectMultiple):

    def render(self, *args, **kwargs):
        output = super().render(*args,**kwargs)
        return mark_safe(output.replace('<ul>', '<p>').replace('</ul>', '</p>')
                         .replace('<li>', '<span>').replace('</li>', '</span>'))


@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    fields = (
        ('name', 'picfile'),
        ('classification', 'texture'),
        ('country', 'city_name'),
        ('lat', 'lng'),
        ('color', 'secondary_colors'),
        'application', 'availability', 'comment', 'maxsize',
        ('maxsize_block_w', 'maxsize_block_h', 'maxsize_block_d'),
        ('maxsize_slab_w', 'maxsize_slab_h'),
        ('hardness', 'uv_resistance'),
        ('created', 'updated'),
    )
    formfield_overrides = {
        models.ManyToManyField: {'widget': HorizCheckboxSelectMultiple},
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 60})},
    }
    readonly_fields = ('created', 'updated', )
    ordering = ('name', )
    list_display = ('name', 'color', 'classification', 'texture', 'country', )
    list_filter = (('classification', RelatedOnlyFieldListFilter),
                   ('color', RelatedOnlyFieldListFilter),
                   ('country', RelatedOnlyFieldListFilter),
                   ('texture', RelatedOnlyFieldListFilter), )
    preserve_filters = True
    search_fields = ['name', ]


@admin.register(StoneName)
class StoneNameAdmin(admin.ModelAdmin):
    ordering = ('name', 'stone', )
    list_display = ('stone', 'name', 'slug', )


class CommonStonePropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'stones_count', 'stones_str')

    def stones_count(self, obj):
        model = obj._meta.model_name
        count = Stone.objects.filter(**{model: obj}).count()
        return count

    def stones_str(self, obj):
        app = obj._meta.app_label
        model = obj._meta.model_name
        stones = [x.name for x in Stone.objects.filter(**{model: obj})]
        stones = ', '.join(stones)
        stones = stones[:120] + '...' if len(stones) > 120 else stones
        ln = reverse('admin:{}_{}_changelist'.format(app, 'stone'))
        param = '?{}__id__exact={}'.format(model, obj.pk)
        ret = '<a href="{}">{}</a>'.format(ln+param, stones)
        return mark_safe(ret)


@admin.register(Color)
class ColorAdmin(CommonStonePropertyAdmin):
    pass


@admin.register(Country)
class CountryAdmin(CommonStonePropertyAdmin):
    pass


@admin.register(Texture)
class TextureAdmin(CommonStonePropertyAdmin):
    pass


@admin.register(Classification)
class ClassificationAdmin(CommonStonePropertyAdmin):
    pass
