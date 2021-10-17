from django.contrib import admin
from .models import Slider

# Register your models here.


class SlideModelAdmin(admin.ModelAdmin):
    list_display = ('title','link','description','image_tag')
    search_fields = ('title','description')
admin.site.register(Slider,SlideModelAdmin)
