from product.models import Product
from django.db import models
from extentions.slug_generator import unique_slug_generator
from django.db.models.signals import pre_save,post_save
# Create your models here.




class Tag(models.Model):
    title = models.CharField(max_length=50,verbose_name='عنوان')
    slug = models.SlugField(max_length=20,verbose_name='آدرس')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    active = models.BooleanField(default=True,verbose_name='فعال/غیر فعال')
    product = models.ManyToManyField(Product,blank=True)

    class Meta:
        verbose_name = 'تگ/برچسب'
        verbose_name_plural = 'تگ/برچسب'

    def __str__(self):
        return self.title

    def product_to_str(self):
        return ','.join([product.title for product in self.product.available()])


def tag_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_reciever,sender=Tag)
