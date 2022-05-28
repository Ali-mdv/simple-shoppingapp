from django.contrib import admin
from .models import ContactUs
# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','is_checked')
    list_filter = ('subject','is_checked')
    search_fields = ('name','email','subject','text')
    list_editable = ('is_checked',)

admin.site.register(ContactUs,ContactUsAdmin)