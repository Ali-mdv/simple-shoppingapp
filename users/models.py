from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
	email = models.EmailField(unique=True,verbose_name='ایمیل')
	phonenumber = PhoneNumberField(unique=True,default='09120000000',verbose_name='شماره همراه')
