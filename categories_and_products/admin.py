from django.contrib import admin

from categories_and_products.models import Category, Product, ProductSales

# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created", "brand")
    list_display = ('name', "created", "id", 'brand')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "category", "brand", "created")
    list_display = ('name', "price", 'brand', "category",
                    "stock", "id", "created","offerPercentage", "active","NewProducts","TopSelling")
    list_display_links = [
        'name',
        'category',
    ]

class ProductSalesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "category", "brand", "created")
    list_display = ('name', "price", 'brand', "category",
                    "stock", "id", "created","offerPercentage", "active","NewProducts","TopSelling")
    list_display_links = [
        'name',
        'category',
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSales, ProductSalesAdmin)