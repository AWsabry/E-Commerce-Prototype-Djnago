<<<<<<< HEAD
from django.contrib import messages
from Register_Login.models import Order, OrderItem, Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


# class Cart(object):
    # @login_required
    # def add_to_cart(request, slug):
    #     context = {}
    #     item = get_object_or_404(Product, slug=slug)
    #     order_item, created = OrderItem.objects.get_or_create(
    #     item=item,
    #     user=request.user,
    #     ordered=False
    # )
    #     order_qs = Order.objects.filter(user=request.user, ordered=False)
    #     if order_qs.exists():
    #         order = order_qs[0]
    #         # check if the order item is in the order
    #         if order.items.filter(item__slug=item.slug).exists():
    #             order_item.quantity += 1
    #             order_item.save()
    #             messages.info(request, "This item quantity was updated.")
    #             return render(request,"home/cart.html",context)
    #         else:
    #             order.items.add(order_item)
    #             messages.info(request, "This item was added to your cart.")
    #             return render(request,"home/cart.html",context)
    #     else:
    #         ordered_date = timezone.now()
    #         order = Order.objects.create(
    #         user=request.user, ordered_date=ordered_date)
    #         order.items.add(order_item)
    #         messages.info(request, "This item was added to your cart.")
    #         return render(request,"home/cart.html",context)


# # # @login_required
# # # def remove_from_cart(request, slug):
# # #     item = get_object_or_404(Product, slug=slug)
# # #     order_qs = Order.objects.filter(
# # #         user=request.user,
# # #         ordered=False
# # #     )
# # #     if order_qs.exists():
# # #         order = order_qs[0]
# # #         # check if the order item is in the order
# # #         if order.items.filter(item__slug=item.slug).exists():
# # #             order_item = OrderItem.objects.filter(
# # #                 item=item,
# # #                 user=request.user,
# # #                 ordered=False
# # #             )[0]
# # #             order.items.remove(order_item)
# # #             order_item.delete()
# # #             messages.info(request, "This item was removed from your cart.")
# # #             return redirect("Register_Login:order-summary")
# # #         else:
# # #             messages.info(request, "This item was not in your cart")
# # #             return redirect("Register_Login:product", slug=slug)
# # #     else:
# # #         messages.info(request, "You do not have an active order")
# # #         return redirect("Register_Login:product", slug=slug)


# # # @login_required
# # # def remove_single_item_from_cart(request, slug):
# # #     item = get_object_or_404(Product, slug=slug)
# # #     order_qs = Order.objects.filter(
# # #         user=request.user,
# # #         ordered=False
# # #     )
# # #     if order_qs.exists():
# # #         order = order_qs[0]
# # #         if order.items.filter(item__slug=item.slug).exists():
# # #             order_item = OrderItem.objects.filter(
# # #                 item=item,
# # #                 user=request.user,
# # #                 ordered=False
# # #             )[0]
# # #             if order_item.quantity > 1:
# # #                 order_item.quantity -= 1
# # #                 order_item.save()
# # #             else:
# # #                 order.items.remove(order_item)
# # #             messages.info(request, "This item quantity was updated.")
# # #             return redirect("Register_Login:order-summary")
# # #         else:
# # #             messages.info(request, "This item was not in your cart")
# # #             return redirect("Register_Login:product", slug=slug)
# # #     else:
# # #         messages.info(request, "You do not have an active order")
# # #         return redirect("Register_Login:product", slug=slug)
=======
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
>>>>>>> 6fe880ad353a2e481ca263bfc625edcc18b9e013
