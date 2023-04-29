from django.contrib import admin
from .models import Order, OrderDetail
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner', 'is_paid', 'jalali_date')
    list_filter = ('is_paid', 'payment_date')
    search_fields = ('owner__username', 'owner__email',
                     'owner__phonenumber', 'ref_id')


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'count')
    search_fields = ('order__owner__username',
                     'order__owner__email', 'product__title')
