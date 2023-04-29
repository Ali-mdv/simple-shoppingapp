from django.contrib import admin
from .models import (Product, Color, ProductGallery,
                     Mattress, IPAdrees, Category, Comment)
from .forms import ProductModelForm
# Register your models here.


@admin.register(Color)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')
    list_filter = ('title',)
    search_fields = ('title',)


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductModelForm
    list_display = ('title', 'image_tag', 'color_to_str',
                    'category_to_str', 'price', 'number', 'status', 'created_humanize')
    list_filter = ('body_color', 'status', 'created')
    search_fields = ('title', 'price', 'body_color__title', 'category__title')
    readonly_fields = ('count_sold', )
    inlines = [ProductGalleryInline, ]


@admin.register(Mattress)
class ProductMattressAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'image_tag')
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_type')
    list_filter = ('title', 'category_type')
    search_fields = ('title',)


@admin.register(Comment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'user__email',
                     'user__phonenumber', 'product__title')


admin.site.register(IPAdrees)
