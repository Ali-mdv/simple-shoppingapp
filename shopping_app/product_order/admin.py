from django.contrib import admin
from .models import Order, OrderDetail
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('owner','is_paid','jalali_date')
    list_filter = ('is_paid','payment_date')
    search_fields = ('owner','ref_id')
admin.site.register(Order,OrderAdmin)



class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order','product','price','count')
    search_fields = ('order','product')
admin.site.register(OrderDetail,OrderDetailAdmin)
