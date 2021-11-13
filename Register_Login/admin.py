from Register_Login.models import BromoCode, Category, Order, OrderItem, Product, Profile
from django.contrib import admin

# Register your models here.


class Register(admin.ModelAdmin):
    list_filter = ("FirstName", "LastName", "last_modified")
    list_display = ('username', "FirstName", 'LastName',
                    "PhoneNumber", "last_modified")


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


class BromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "code",)
    list_display = ('code', "percentage", 'created', "active")


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'delivered',
                    'coupon',
                    'ordered_date'

                    ]
    list_display_links = [
        'user',
        'coupon'
    ]
    list_filter = ['ordered',
                   'delivered',
                   'ordered_date',
                   ]
    inlines = [
        OrderItemAdmin,
    ]


admin.site.register(Profile, Register)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BromoCode, BromoCodeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
