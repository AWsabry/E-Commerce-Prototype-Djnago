from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Order

from categories_and_products.models import BromoCode

# Register your models here.



    
    
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


class BromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "code",)
    list_display = ('code', "percentage", 'created', "active")


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems)
admin.site.register(BromoCode, BromoCodeAdmin)