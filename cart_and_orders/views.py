from django.shortcuts import redirect, render
from Register_Login.models import Profile
from cart_and_orders.forms import BromoCodeForm

from cart_and_orders.models import Cart, CartItems, Order
from categories_and_products.models import BromoCode, Category, Product

# Create your views here.


def cart(request):
    discountform = BromoCodeForm(
        request.POST, use_required_attribute=False,)
    products = Product.objects.filter(active=True,).values()
    bromocode = BromoCode.objects.filter(active=True,).values()
    categories = Category.objects.filter(active=True)
    userLoggedIN = Profile.objects.filter(id=request.user.id).first()
    cartItem = CartItems.objects.filter(
        user=request.user, ordered=False).values()

    # Sum of order
    totalOrderPricelist = []
    for totalPriceCheck in cartItem:
        totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    total = sum(totalOrderPricelist)

    # getting bromocode name
    for sytax in bromocode:
        code = sytax['code']

    context = {
        "products": products,
        "categories": categories,
        'userLoggedIN': userLoggedIN,
        'cartItem': cartItem,
        'form': discountform,
        'total': total,
    }

    if request.method == 'POST':
        total = total * sytax['percentage']
        context['total'] = total
        Order.objects.create(
            user=request.user,
            ordered=False,
            totalPrice=total,
        )

        return redirect('ThankYou')

    return render(request, 'cart.html', context)


def checkout(request):
    discountform = BromoCodeForm(
        request.POST)
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

    # Sum of order
    totalOrderPricelist = []
    for totalPriceCheck in cartItem:
        totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    total = sum(totalOrderPricelist)

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
        'cartItems' : cartItems
    }
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        total = total * sytax['percentage']
        context['total'] = total
        print(request.user)
        print(cart)
        Order.objects.create(
            user=request.user,
            totalPrice=total,
            coupon='H',
            cart=cart,
        )
        CartItems.objects.update(
            ordered=True,
        )
        #  CartItems.objects.filter(user=request.user).delete()

        return redirect('/thankyou')
    return render(request, 'checkout.html', context)


def ThankYou(request):
    return render(request, 'thankyou.html')
