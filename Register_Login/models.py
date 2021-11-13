from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid


class Profile(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    FirstName = models.CharField(max_length=50, default='', null=True)
    LastName = models.CharField(max_length=50, default='', null=True)
    Age = models.CharField(max_length=10, default='', null=True)
    PhoneNumber = models.IntegerField()
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
    oldPrice = models.FloatField(blank=True, null=True)
    offerPercentage = models.IntegerField(blank=True, null=True,)
    active = models.BooleanField(default=True)
    TopSelling = models.BooleanField(default=False)
    NewProducts = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()

    def get_absolute_url(self):
        return reverse("productDetails", args=[self.slug])
    
    def discountpercentage(self):
        discountAmount = self.oldPrice - self.price
        self.offPercentage = (discountAmount/self.oldPrice) * 100
        return (int(self.offPercentage))
    offerPercentage = property(discountpercentage)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class BromoCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          editable=False)
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


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        BromoCode, on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    comment = models.TextField(max_length=2000,blank=True,null=True)
    totalPrice = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class OrderItem(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.IntegerField(default=1,name='quantity')
    created = models.DateTimeField(auto_now_add=True)
    totalOrderItemPrice = models.PositiveIntegerField(default=0)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return f"{self.quantity} | {self.product} from {self.user} at {self.created}  "
         