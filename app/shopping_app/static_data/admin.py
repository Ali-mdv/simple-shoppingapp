from django.contrib import admin
from .forms import SiteInfoForm
from .models import (
    SiteInfo
)
# Register your models here.


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    form = SiteInfoForm
    list_display = ("local_name", "english_name",
                    "phonenumber", "email", "domain", "status")
