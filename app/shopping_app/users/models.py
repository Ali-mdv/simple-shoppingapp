from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from product.models import Product
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phonenumber = PhoneNumberField(unique=True, verbose_name='شماره همراه')


class UserAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=155)
    post_code = models.CharField(max_length=20)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "لیست آدرس ها"

    def save(self, *args, **kwargs):
        if self.user.useraddress_set.count() > 3:
            raise ValidationError("each user can have 3 address")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.address


class UserWishList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True
    )
    items = models.ManyToManyField(Product, verbose_name="محصولات")

    class Meta:
        verbose_name = "علاقه مندی"
        verbose_name_plural = "لیست علاقه مندی"

    def __str__(self):
        return self.user.username

    def contains(self, product_id):
        if (self.items.filter(pk=product_id).exists()):
            return True
        return False

    def items_to_str(self):
        return ", ".join([item.title for item in self.items.all()])
    items_to_str.short_description = "اقلام"
