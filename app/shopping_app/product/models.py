import uuid
from django.db import models
from colorfield.fields import ColorField
# from djmoney.models.fields import MoneyField
from django.utils.html import format_html
from extentions.utils import change_image_size
from django.contrib.humanize.templatetags.humanize import naturalday
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

# Create your Manager here.


class ProductManager(models.Manager):
    def available(self):
        return self.order_by("-status")


# Create your models here.

class Color(models.Model):
    title = models.CharField(max_length=20, verbose_name='اسم رنگ')
    slug = models.SlugField(unique=True, max_length=60,
                            verbose_name='آدرس', blank=True)
    color = ColorField(default='#FF0000', verbose_name='رنگ')
    status = models.BooleanField(default=False, verbose_name='وضعیت موجودی')

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ'

    def __str__(self):
        return self.title


class IPAdrees(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آی پی آدرس')

    def __str__(self):
        return self.ip_address


class Category(models.Model):
    parent = models.ForeignKey(
        "self", default=None, blank=True, null=True,
        on_delete=models.SET_NULL, related_name="children", verbose_name="زیر دسته"
    )
    title = models.CharField(max_length=60, verbose_name='عنوان')
    slug = models.CharField(unique=True, max_length=60, verbose_name='آدرس')
    status = models.BooleanField(default=False, verbose_name='وضعیت موجودی')
    is_parent = models.BooleanField(
        default=False, verbose_name="آیا دسته بندی اصلی می باشد؟")

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self) -> str:
        return self.title

    def sub_categoty_products(self):
        if self.is_parent:
            childs = self.children.filter(status=True)
            products = Product.objects.select_related(
                "category").prefetch_related(
                'color').filter(
                category__in=childs)
            return products
        return None


class Product(models.Model):
    title = models.CharField(max_length=60, verbose_name="عنوان")
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    image = models.ImageField(upload_to='products', verbose_name='عکس')
    introduction = models.TextField(verbose_name='معرفی اجمالی')
    price = models.DecimalField(
        max_digits=11, decimal_places=0, verbose_name='قیمت')
    color = models.ManyToManyField(Color, verbose_name='رنگ')
    number = models.IntegerField(default=0, verbose_name='تعداد')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="دسته بندی")
    weight = models.DecimalField(null=True, blank=True,
                                 max_digits=5, decimal_places=1, verbose_name="وزن")
    dimensions = models.CharField(
        null=True, blank=True, max_length=20, verbose_name="ابعاد")
    other_description = models.TextField(null=True, blank=True,
                                         max_length=500, verbose_name='توضیحات دیگر')
    status = models.BooleanField(default=False, verbose_name='وضعیت موجودی')
    created = models.DateTimeField(
        auto_now=True, verbose_name='زمان', editable=False)
    hits = models.ManyToManyField(
        IPAdrees, blank=True, verbose_name='بازدید', editable=False)
    is_special = models.BooleanField(default=False, verbose_name='محصول ویژه')
    discount = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.0, verbose_name="تخفیف")
    count_sold = models.IntegerField(
        default=0, verbose_name="تعداد فروخته شده")
    ratings = GenericRelation(Rating, related_query_name='rate')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def image_tag(self):
        return format_html('<img src="{}" width=60px height=70px>'.format(self.image.url))
    image_tag.short_description = 'عکس'

    def created_humanize(self):
        natural_time = naturalday(self.created)
        return natural_time
    created_humanize.short_description = 'تاریخ ایجاد'

    def color_to_str(self):
        return ", ".join([color.title for color in self.color.all()])
    color_to_str.short_description = "رنگ"

    def get_total_price(self):
        return round(self.price - self.price * self.discount if self.is_special else self.price)

    def get_discount_percent(self):
        return round(self.discount * 100)

    def check_availability(self):
        if self.number <= 0:
            self.status = False

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.uuid])

    objects = ProductManager()


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the category.
    """
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, verbose_name='دسته بندی')
    attribute = models.CharField(max_length=255, verbose_name='ویژگی')

    def __str__(self):
        return self.attribute


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual attribute or bespoke features.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='specifications', verbose_name='محصول')
    specification = models.ForeignKey(
        ProductSpecification, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=255, verbose_name='مقدار')

    def __str__(self):
        return self.value


class ProductGallery(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galleries', verbose_name='عکس')

    class Meta:
        verbose_name = 'گالری محصول'
        verbose_name_plural = 'گالری محصولات'

    def __str__(self):
        return self.image.name


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments", verbose_name="محصول")
    text = models.TextField(verbose_name="دیدگاه")
    date = models.DateTimeField(auto_now=True, verbose_name="تاریخ ایجاد")
    rating = models.IntegerField(validators=[MaxValueValidator(
        5), MinValueValidator(0), ], blank=True, null=True, verbose_name="امتیاز")
    status = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.product.title}, {self.user.username}"

    def date_humanize(self):
        natural_time = naturalday(self.date)
        return natural_time