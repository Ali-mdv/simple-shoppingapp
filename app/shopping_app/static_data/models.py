from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class SiteInfo(models.Model):
    local_name = models.CharField(max_length=50, verbose_name="نام فروشگاه")
    english_name = models.CharField(
        max_length=50, verbose_name="نام فروشگاه به انگلیسی")
    phonenumber = PhoneNumberField(
        null=True, blank=True, verbose_name='تلفن همراه')
    landline = PhoneNumberField(
        null=True, blank=True, verbose_name="تلفن ثابت")
    email = models.EmailField(max_length=50, verbose_name="ایمیل")
    address = models.TextField(max_length=100, verbose_name="آدرس فروشگاه")
    domain = models.CharField(max_length=50,default="localhost", verbose_name="دامنه سایت")
    telegram_link = models.URLField(null=True, blank=True, verbose_name="آدرس تلگرام")
    instagram_link = models.URLField(null=True, blank=True, verbose_name="آدرس اینستاگرام")
    whatsapp_link = models.URLField(null=True, blank=True, verbose_name="آدرس واتساپ")
    status = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'اطلاعات فروشگاه اینترنتی'
        verbose_name_plural = 'اطلاعات فروشگاه اینترنتی'

    def __str__(self):
        return self.local_name

    def save(self, *args, **kwargs):
        # There should be only one instance with "True" status
        if self.status:
            SiteInfo.objects.filter(status=True).update(status=False)

        super().save(*args, **kwargs)
