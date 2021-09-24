from typing import Reversible
from django.contrib.auth.forms import UserModel
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse



class Profile(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    FirstName = models.CharField(max_length=50, default='', null=True)
    LastName = models.CharField(max_length=50, default='', null=True)
    Age = models.CharField(max_length=10, default='', null=True)
    PhoneNumber = models.IntegerField(max_length=50, default='', null=True)
    last_modified = models.DateTimeField(auto_now=True)
    ProfilePic = models.ImageField(upload_to="profile/", null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.FirstName} ({self.LastName})"

class Category(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    image = models.ImageField(upload_to="categories", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        return reverse("product_detail", args= [self.slug])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, db_index=True,)
    image = models.ImageField(upload_to="products", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()

    def get_absolute_url(self):
        return reverse("product_detail", args= [self.slug])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = "Products"

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    total_price=  models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    order_code = models.CharField(max_length=10, blank = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} "


    def get_total_cost(self):
        OrderData = OrderItem()
        self.total=0
        for prodcut in OrderData:
            self.total += prodcut.total_cost()
        return sum(OrderData.get_cost() for item in self.items.all())

    class Meta:
        verbose_name_plural = "Orders"

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    orders = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='item')
    quantity = models.IntegerField(default=1)
    comment = models.TextField(blank=True)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product} {self.quantity} "

    def get_cost(self):
        return self.product.price * self.quantity


class BromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True,blank = True)
    percentage = models.FloatField(default = 0.0)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
        
    def save(self, *args, **kwargs):
        self.percentage = round(self.percentage, 2)
        super(BromoCode, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "BromoCodes"