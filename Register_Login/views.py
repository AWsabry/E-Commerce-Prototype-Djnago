from django.db import models
from django.http import request
from Register_Login.models import BromoCode, Category, Order, OrderItem, Product, Profile
from Register_Login.forms import BromoCodeForm, CompleteProfile, LoginForm, QuantityForm, RegisterForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime


def Register(request):
    form = RegisterForm(request.POST, request.FILES)
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('completeProfile')
        return render(request, "home/Register.html",  {
            'form': form
        })


def completeProfile(request):
    form = CompleteProfile(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.username = request.user
            context = {}
            context['form'] = form
            form.save()
            return redirect('index')
    return render(request, "home/completeProfile.html",  {
        'form': form,
    })


def logOut(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'home/LogOut.html')


def index(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)
        userLoggedIN = Profile.objects.filter(username=request.user).first()
        context = {
            "products": products,
            "categories": categories,
            'userLoggedIN': userLoggedIN,
        }
        return render(request, 'home/index.html', context)
    else:
        return redirect('sign')


@login_required
def product_detail(request, slug):
    quantityForm = QuantityForm(request.POST)
    products = Product.objects.filter(
        slug=slug, active=True,).first()
    date = datetime.datetime.now().hour
    user = Profile.objects.filter(username=request.user).first()
    order_item = OrderItem.objects.filter(
        user=request.user, ordered=False).values()

    context = {
        "name": products.name,
        "category": products.category,
        "price": products.price,
        "description": products.description,
        "stock": products.stock,
        'date': date,
        'form': quantityForm,
    }
    if request.method == 'POST':
        if quantityForm.is_valid():
            totalOrderItemPrice = products.price * \
                quantityForm.cleaned_data['Quantity']
            OrderItem.objects.create(
                product=products,
                user=request.user,
                ordered=False,
                quantity=quantityForm.cleaned_data['Quantity'],
                totalOrderItemPrice=totalOrderItemPrice
            )
            return redirect('cart')

    else:
        return render(request, "home/product_detail.html", context, )


def cart(request):
    discountform = BromoCodeForm(
        request.POST, use_required_attribute=False,)
    products = Product.objects.filter(active=True,).values()
    bromocode = BromoCode.objects.filter(active=True,).values()
    categories = Category.objects.filter(active=True)
    userLoggedIN = Profile.objects.filter(username=request.user).first()
    order_item = OrderItem.objects.filter(
        user=request.user, ordered=False,).values()

    # Sum of order
    totalOrderPricelist = []
    for totalPriceCheck in order_item:
        totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    total = sum(totalOrderPricelist)

    # getting bromocode name
    for sytax in bromocode:
        code = sytax['code']

    context = {
        "products": products,
        "categories": categories,
        'userLoggedIN': userLoggedIN,
        'order_item': order_item,
        'form': discountform,
        'total': total
    }
    orderItemList = []
    for i in order_item:
        orderItemList.append(i['id'])
    x = orderItemList

    print(x)
    if request.method == 'POST':
        if discountform.is_valid():
            if discountform.cleaned_data['code'] == code:
                total = total * sytax['percentage']
                context['total'] = total
                order = Order.objects.create(
                user=request.user,
                ordered=False,
                totalPrice=total,
                coupon=BromoCode.objects.get(code=code),
            )            
            print(OrderItem.objects.filter(user=request.user, ordered=False).values())
            order.items.set(x)



            OrderItem.objects.filter(
                user=request.user, ordered=False).update(ordered=True,)

            return redirect('done')

    return render(request, 'home/cart.html', context)


def done(request):
    return render(request, 'home/done.html')


def sign(request):
    form = LoginForm(request.POST, request.FILES)
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('index')
        return render(request, 'home/signin.html', {'form': form})
