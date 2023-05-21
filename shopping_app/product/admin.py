from django.contrib import admin
from .models import (
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    Color,
    ProductGallery,
    IPAdrees,
    Category,
    Comment
)
# from .forms import ProductModelForm
# Register your models here.


@admin.register(Color)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'color')
    list_filter = ('title',)
    search_fields = ('title',)


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # form = ProductModelForm
    list_display = ('title', 'image_tag', 'color_to_str', 'category',
                    'price', 'number', 'status', 'created_humanize')
    list_filter = ('category', 'status', 'created')
    search_fields = ('title', 'price', 'color__title', 'category__title')
    readonly_fields = ('count_sold', )
    inlines = [ProductSpecificationValueInline, ProductGalleryInline]


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    list_filter = ('title',)
    search_fields = ('title',)
    inlines = [
        ProductSpecificationInline
    ]


@admin.register(Comment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'user__email',
                     'user__phonenumber', 'product__title')


admin.site.register(IPAdrees)
