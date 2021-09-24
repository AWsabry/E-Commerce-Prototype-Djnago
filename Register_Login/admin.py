from Register_Login.models import BromoCode, Category, Order, OrderItem, Product, Profile
from django.contrib import admin

# Register your models here.

class Register(admin.ModelAdmin):
    list_filter = ("FirstName", "LastName", "last_modified")
    list_display = ('username', "FirstName",'LastName',"PhoneNumber", "last_modified")


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created", "brand")
    list_display = ('name', "created",'brand')

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "category", "brand","created")
    list_display = ('name', "price",'brand',"category","stock","created","active")

class OrderAdmin(admin.ModelAdmin):
    list_filter = ("user", "paid","created")
    list_display = ("user", "total_price", "paid","created")


class BromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "code",)
    list_display = ('code', "percentage",'created',"active")


admin.site.register(Profile,Register)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(BromoCode,BromoCodeAdmin)

