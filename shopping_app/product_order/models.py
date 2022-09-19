from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models.manager import Manager
from django.core.exceptions import ObjectDoesNotExist
from users.models import User, UserAddress
from product.models import Product


# Create your models here.

class OrderManager(Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None


class Order(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    payment_date = models.DateTimeField(
        verbose_name='تاریخ پرداخت', null=True, blank=True)
    ref_if = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='کد پیگیری')
    address = models.ForeignKey(
        UserAddress, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='آدرس')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'

    def __str__(self):
        return self.owner.get_full_name()

    def total_price_order(self):
        total = 0
        for detail in self.orderdetail_set.all():
            total += detail.count * detail.price

        return total

    objects = OrderManager()


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='محصول')
    price = MoneyField(verbose_name='قیمت', max_digits=9,
                       decimal_places=0, default_currency='IRR')
    count = models.PositiveIntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'جزییات سبد های خرید'

    def __str__(self):
        return self.product.title

    def total_price_detail(self):
        return self.count * self.product.price
