from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Order

from categories_and_products.models import BromoCode

    
    
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
                    'ordered_date'

                    ]
    list_display_links = [
        'user',
    ]
    list_filter = ['user','ordered',
                   'delivered',
                   'ordered_date',
                   ]


class BromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "code",)
    list_display = ('code', "percentage", 'created', "active")


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItems)
admin.site.register(BromoCode, BromoCodeAdmin)