from django.db import models

# Create your models here.


class ContactUs(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام')
    email = models.EmailField(max_length=100,verbose_name='ایمیل')
    subject = models.CharField(max_length=100,verbose_name='موضوع')
    text = models.TextField(verbose_name='متن')
    is_checked = models.BooleanField(default=False,verbose_name='چک شده')

    class Meta:
        verbose_name = 'ارتباط با ما'
        verbose_name_plural = 'ارتباطات با ما'


    def __str__(self):
        return self.subject