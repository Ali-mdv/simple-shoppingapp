from django.contrib import admin
from .models import Tag
# Register your models here.


class TagModelAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_at','product_to_str')
    list_filter = (('title','slug','created_at'))
    search_fields = ('title',)


admin.site.register(Tag,TagModelAdmin)