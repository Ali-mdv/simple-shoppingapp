from django.db import models
from colorfield.fields import ColorField
from djmoney.models.fields import MoneyField
from django.utils.html import format_html
from extentions.utils import change_name
from extentions.slug_generator import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import  reverse
from django.contrib.humanize.templatetags.humanize import naturalday
from django.db.models import Q
# Create your Manager here.

class ProductManager(models.Manager):
	def available(self):
		return self.filter(status=True)
		# return self.filter(number = True)


# Create your models here.

class Color(models.Model):
	title = models.CharField(max_length=20,verbose_name='اسم رنگ')
	slug = models.SlugField(unique=True,max_length=60,verbose_name='آدرس',blank=True)
	color = ColorField(default='#FF0000',verbose_name='رنگ')
	status = models.BooleanField(default=False,verbose_name='وضعیت موجودی')
	
	class Meta:
		verbose_name = 'رنگ'
		verbose_name_plural = 'رنگ'

	def __str__(self):
		return self.title


class Texture(models.Model):
	title = models.CharField(max_length=50,verbose_name='بافت')
	slug = models.SlugField(unique=True,max_length=60,verbose_name='آدرس',blank=True)
	tie = models.IntegerField(verbose_name='تعداد گره',blank=True,null=True)
	status = models.BooleanField(default=False,verbose_name='وضعیت موجودی')
	class Meta:
		verbose_name = 'بافت'
		verbose_name_plural = 'بافت'

	def __str__(self):
		return self.title


class Pattern(models.Model):
	title = models.CharField(max_length=50,verbose_name='مدل')
	slug = models.SlugField(unique=True,max_length=60,verbose_name='آدرس',blank=True)
	two_poeple = models.BooleanField(default=False,null=True,blank=True,verbose_name='دو نفره')
	status = models.BooleanField(default=False,verbose_name='وضعیت موجودی')


	class Meta:
		verbose_name = 'مدل'
		verbose_name_plural = 'مدل'

	def __str__(self):
		return self.title


class Mattress(models.Model):
	title = models.CharField(max_length=120,verbose_name='عنوان')
	color = models.ForeignKey(Color, on_delete=models.CASCADE,verbose_name='رنگ تشک')
	image = models.ImageField(upload_to='mattress',verbose_name='عکس')

	class Meta:
		verbose_name = 'تشک'
		verbose_name_plural = 'تشک ها'

	def __str__(self):
		return self.title
		
	def image_tag(self):
		return format_html('<img src="{}" width=80px height=50px>'.format(self.image.url))
	image_tag.short_description = 'عکس'


class IPAdrees(models.Model):
	ip_address = models.GenericIPAddressField(verbose_name='آی پی آدرس')

	def __str__(self):
		return self.ip_address


class Product(models.Model):
	slug = models.SlugField(unique=True,max_length=60,verbose_name='آدرس',blank=True)
	image = models.ImageField(upload_to='products',verbose_name='عکس')
	description = models.TextField(max_length=500,verbose_name='توضیحات')
	price = MoneyField(verbose_name='قیمت', max_digits=9, decimal_places=0, default_currency='IRR')
	pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE,verbose_name='مدل')
	body_color = models.ForeignKey(Color, on_delete=models.CASCADE,verbose_name='رنگ بدنه')
	mattress = models.ManyToManyField(Mattress, verbose_name="تشک")
	texture = models.ForeignKey(Texture, on_delete=models.CASCADE,verbose_name='بافت')
	number = models.IntegerField(default=0,verbose_name='تعداد')
	status = models.BooleanField(default=False,verbose_name='وضعیت موجودی')
	created = models.DateTimeField(auto_now=True,verbose_name='زمان')
	is_special = models.BooleanField(default=False,verbose_name='محصول ویژه')
	hits = models.ManyToManyField(IPAdrees,blank=True,verbose_name='بازدید')

	class Meta:
		verbose_name = 'محصول'
		verbose_name_plural = 'محصول'
		ordering = ['-created']

	def __str__(self):
		return f'تاب ریلکسی مدل {self.pattern}'


	def title(self):
		return f'تاب ریلکسی مدل {self.pattern}'
	title.short_description = 'عنوان'

	def image_tag(self):
		return format_html('<img src="{}" width=80px height=50px>'.format(self.image.url))
	image_tag.short_description = 'عکس'


	def created_humanize(self):
		natural_time = naturalday(self.created)
		return natural_time
	created_humanize.short_description = 'تاریخ ایجاد'


	def check_availabity(self):
		if self.number == 0:
			self.status = False
		else:
			self.status = True

	# def get_absolute_url(self):
	# 	return reverse('product:detail',kwargs={'slug':self.slug})


	objects = ProductManager()


class ProductGallery(models.Model):
	title = models.CharField(max_length=120,verbose_name='عنوان')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='galleries',verbose_name='عکس')

	class Meta:
		verbose_name = 'عکس'
		verbose_name_plural = 'عکس'

	def __str__(self):
		return self.image.name



# => generate unique slug for each instance from product model
# def product_pre_save_slug(sender,instance,*args,**kwargs):
# 	if not instance.slug:
# 		instance.slug = unique_slug_generator(instance)

# pre_save.connect(product_pre_save_slug,sender=Product)
