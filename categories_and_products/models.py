from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
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
    slug = models.SlugField(unique=True, db_index=True,)
    image = models.ImageField(upload_to="products", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    oldPrice = models.FloatField(blank=True, null=True,default=0)
    offerPercentage = models.FloatField(blank=True, null=True,)
    active = models.BooleanField(default=True)
    TopSelling = models.BooleanField(default=False)
    NewProducts = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()

    def get_absolute_url(self):
        return reverse("productDetails", args=[self.slug])
    
    def discountpercentage(self):
        if self.oldPrice :
            discountAmount = self.oldPrice - self.price
            self.offPercentage = (discountAmount/self.oldPrice) * 100
            return (int(self.offPercentage))
        else:
            pass
    offerPercentage = property(discountpercentage)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class BromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True,null=True)
    percentage = models.FloatField(default=0.0, validators=[
                                   MinValueValidator(0.0), MaxValueValidator(1.0)],)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.percentage = round(self.percentage, 2)
        super(BromoCode, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "BromoCodes"
