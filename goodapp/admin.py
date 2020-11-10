from django.contrib import admin

from .models import Good, Picture, Manufacturer, Category

class PictureInline(admin.TabularInline):

    model = Picture

    fields = (
    			'image_url',
    			'main_image',
    	)

    exclude = ('title', 'slug')
    extra = 0


class GoodAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					'good_uid',
					'price',
					'article',
					'dimensions',
					'razmer_kpb',
					'razmer_navolocek',
					'tip_prostyni',
					'upakovka',
					'fabric',
					'duvet_cover_size',
					'quantity',
					'weight',
					'is_active',
					'manufacturer',
					'parent_good',
					)

	list_filter = ('category', 'manufacturer')

	inlines 	 = [PictureInline, ]

	exclude = ('slug', 'cpu_slug')

admin.site.register(Good, GoodAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					)
	
	exclude = ('slug', 'cpu_slug')

admin.site.register(Manufacturer, ManufacturerAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					)
	
	exclude = ('slug', 'cpu_slug')

admin.site.register(Category, CategoryAdmin)