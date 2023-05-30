from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAddress, UserWishList
# Register your models here.


admin.site.register(User, UserAdmin)

UserAdmin.fieldsets[1][1]['fields'] = (
    'first_name', 'last_name', 'email', 'phonenumber')


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "address", "post_code")
    search_fields = ('user__username', 'user__email',
                     'user__phonenumber', "address", "post_code")


@admin.register(UserWishList)
class UserWishListAdmin(admin.ModelAdmin):
    list_display = ("user", "items_to_str")
    search_fields = ('user__username', 'user__email',
                     'user__phonenumber',)
