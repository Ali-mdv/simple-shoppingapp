from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


admin.site.register(User,UserAdmin)

UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'phonenumber')