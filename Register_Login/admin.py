from Register_Login.models import Category, Product, RegisterationModel
from django.contrib import admin

# Register your models here.

class Register(admin.ModelAdmin):
    list_filter = ("FirstName", "LastName", "last_modified")
    list_display = ('username', "FirstName",'LastName',"PhoneNumber", "last_modified")


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ("name", "created", "brand")
    list_display = ('name', "created",'brand')

class ProductAdmin(admin.ModelAdmin):
    list_filter = ("name", "category", "brand","created")
    list_display = ('name', "price",'brand',"category","stock","created","active")


admin.site.register(RegisterationModel,Register)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)

