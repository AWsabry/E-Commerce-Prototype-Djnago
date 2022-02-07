from Register_Login.models import BromoCode, Cart, Category, Order, Product, Profile,CartItems
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




    
    
class CartItemsAdmin(admin.TabularInline):
    model = CartItems
    raw_id_fields = ['product']
    

class CartAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'total_price',
                    'delivered',
                    'coupon',
                    'ordered_date',
                    'paid'

                    ]
    inlines = [
        CartItemsAdmin,
    ]
    
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'delivered',
                    # 'coupon',
                    'ordered_date'

                    ]
    list_display_links = [
        'user',
        # 'coupon'
    ]
    list_filter = ['ordered',
                   'delivered',
                   'ordered_date',
                   ]
    # inlines = [
    #     CartItemsAdmin,
    # ]


admin.site.register(Profile, Register)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BromoCode, BromoCodeAdmin)
admin.site.register(Order, OrderAdmin)

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems)
