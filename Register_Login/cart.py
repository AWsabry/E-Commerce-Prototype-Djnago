from django.conf import settings
from .models import Product


class Cart(object):

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')


    def addProduct(self, product, quantity=1, update_quantity=False,comment='',order_arrive_time=0,order_code = ""):
        product_id = int(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price),
                                      'comment':comment,
                                      'order_arrive_time':order_arrive_time,
                                      'order_code':order_code}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['order_arrive_time'] = order_arrive_time
            self.cart[product_id]['comment']    = comment
            self.cart[product_id]['order_code'] = order_code
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self,product):
        product_id = str(product.id)


    def __iter__(self):

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clearCart(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())
