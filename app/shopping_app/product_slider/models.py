from django.db import models
from django.utils.html import format_html
from extentions.utils import change_image_size

# Create your models here.


class Slider(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    link = models.URLField(max_length=50, verbose_name='لینک')
    description = models.TextField(
        max_length=50, verbose_name='توضیحات', blank=True)
    image = models.ImageField(upload_to='sliders', verbose_name='عکس')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلاید'

    def __str__(self):
        return self.title

    def image_tag(self):
        return format_html('<img src="{}" width=70px height=60px>'.format(self.image.url))

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     image = change_image_size(self.image.path, 920, 380)
    #     image.save(self.image.path)
