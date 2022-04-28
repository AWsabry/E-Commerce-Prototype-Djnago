from django.shortcuts import redirect, render
from sqlalchemy import false
from Register_Login.forms import RegisterForm
from Register_Login.models import Profile
from cart_and_orders.forms import BromoCodeForm

from cart_and_orders.models import Cart, CartItems, Order
from categories_and_products.models import BromoCode, Category, Product

# Create your views here.


def checkout(request):
    discountform = BromoCodeForm(request.POST)

    userProfile = Profile.objects.filter(id=request.user.id).first()
    products = Product.objects.filter(active=True,).values()
    bromocode = BromoCode.objects.filter(active=True,).values()
    categories = Category.objects.filter(active=True)
    userLoggedIN = Profile.objects.filter(id=request.user.id).first()

    cartItem = CartItems.objects.filter(
        user=request.user, ordered=False).values()

    cartItems = CartItems.objects.filter(
        user=request.user, ordered=False)

    cart = Cart.objects.filter(user=request.user).values()

    # OrderItem_id
    for getting_Id in cartItem:
        cartItem_id = getting_Id['id']

    cartItem
    # print(cartItem)

    # Sum of order
    totalOrderPricelist = []
    for totalPriceCheck in cartItem:
        totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    total = sum(totalOrderPricelist)

    print(total)

    # getting bromocode name
    for sytax in bromocode:
        code = sytax['code']

    context = {
        "products": products,
        "categories": categories,
        'userLoggedIN': userLoggedIN,
        'cartItem': cartItem,
        'form': discountform,
        'cart': cart,
        'total': total,
        'userProfile': userProfile,
        'cartItems': cartItems
    }
    cart = Cart.objects.get(user=request.user)

    if request.method == 'POST':

        total = total * sytax['percentage']
        context['total'] = total

        print(sytax['percentage'])

        if discountform.is_valid():
            Order.objects.create(
                user=request.user,
                totalPrice=total,
                BromoCode=discountform.cleaned_data['code'],
                cart=cart,
            

            )

        order = Order.objects.filter(
            user=request.user, delivered=False, paid=False).values()

        for getting_Id in order:
            order_id = getting_Id['id']
        order_id
        print(order_id)
        

        CartItems.objects.filter(user=request.user, id=cartItem_id).update(
            ordered=True,
            orderId=order_id,
        )
        Cart.objects.filter(user=request.user).update(total_price=0)


        return redirect('/thankyou')
    return render(request, 'checkout.html', context)


def ThankYou(request):
    return render(request, 'thankyou.html')
