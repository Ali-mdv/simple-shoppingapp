from django.contrib import admin
from .models import Product, Color, ProductGallery, Mattress, IPAdrees, Category, Comment
# Register your models here.


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')
    list_filter = ('title',)
    search_fields = ('title',)


admin.site.register(Color, ProductColorAdmin)


class PropertyGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'color_to_str',
                    'category_to_str', 'price', 'number', 'status', 'created_humanize')
    list_filter = ('price', 'body_color', 'number',
                   'status', 'created')
    search_fields = ('price', 'body_color', 'category_to_str')
    inlines = [PropertyGalleryInline, ]


admin.site.register(Product, PropertyAdmin)


class ProductMattressAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'image_tag')
    list_filter = ('title',)
    search_fields = ('title',)


admin.site.register(Mattress, ProductMattressAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_type')
    list_filter = ('title', 'category_type')
    search_fields = ('title',)


admin.site.register(Category, ProductCategoryAdmin)


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')


admin.site.register(Comment, ProductCommentAdmin)

admin.site.register(IPAdrees)
