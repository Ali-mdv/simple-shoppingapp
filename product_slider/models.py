from django.db import models
from django.utils.html import format_html

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=50,verbose_name='عنوان')
    link = models.URLField(max_length=50,verbose_name='لینک')
    description = models.TextField(max_length=50,verbose_name='توضیحات',blank=True)
    image = models.ImageField(upload_to='sliders',verbose_name='عکس')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلاید'

    def __str__(self):
        return self.title

    def image_tag(self):
        return format_html('<img src="{}" width=80px height=50px>'.format(self.image.url))
