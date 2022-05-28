from django.contrib import admin
from .models import Product,Color,Texture,ProductGallery,Pattern,Mattress,IPAdrees
# Register your models here.


class ProductColorAdmin(admin.ModelAdmin):
	list_display = ('title', 'color')
	list_filter = ('title',)
	search_fields = ('title',)
admin.site.register(Color,ProductColorAdmin)


class ProducTextureAdmin(admin.ModelAdmin):
	list_display = ('title', 'tie')
	list_filter = ('title',)
	search_fields = ('title',)
admin.site.register(Texture,ProducTextureAdmin)


class ProducPatternAdmin(admin.ModelAdmin):
	list_display = ('title', 'two_poeple')
	list_filter = ('title',)
	search_fields = ('title',)
admin.site.register(Pattern,ProducPatternAdmin)


class PropertyGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
	list_display = ('title', 'image_tag', 'body_color','texture', 'pattern', 'price', 'number', 'status', 'created_humanize')
	list_filter = ('price', 'body_color', 'number','pattern', 'status', 'created')
	search_fields = ('price', 'body_color','pattern')
	inlines = [ PropertyGalleryInline, ]

admin.site.register(Product, PropertyAdmin)

class ProductMattressAdmin(admin.ModelAdmin):
	list_display = ('title', 'color','image_tag')
	list_filter = ('title',)
	search_fields = ('title',)
admin.site.register(Mattress,ProductMattressAdmin)




admin.site.register(IPAdrees)