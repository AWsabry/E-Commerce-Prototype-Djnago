from typing import Reversible
from django.contrib.auth.forms import UserModel
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse


class RegisterationModel(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    FirstName = models.CharField(max_length=50, default='', null=True)
    LastName = models.CharField(max_length=50, default='', null=True)
    Age = models.CharField(max_length=10, default='', null=True)
    PhoneNumber = models.CharField(max_length=50, default='', null=True)
    last_modified = models.DateTimeField(auto_now=True)
    ProfilePic = models.ImageField(upload_to="profile/", null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.FirstName} ({self.LastName})"

# def create_user(sender,**kwargs):
#     if kwargs['created']:
#         user_client=RegisterationModel.objects.filter(username=kwargs['instance'])
# post_save.connect(create_user,sender=User)


class Category(models.Model):
    name = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to="categories", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to="products", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()

    def get_absolute_url(self):
        return Reversible("product_detail", args= [self.id])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = "Products"
