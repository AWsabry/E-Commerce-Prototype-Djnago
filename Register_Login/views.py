from django.http.response import HttpResponse
from rest_framework.response import Response
from Register_Login.models import BromoCode, Cart, CartItems, Category, Order, Product, Profile
from Register_Login.forms import BromoCodeForm, CompleteProfile, LoginForm, QuantityForm, RegisterForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from rest_framework.views import APIView
from rest_framework import status
from Register_Login.serializers import Profileserializers


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
            Cart.objects.create(
                user=request.user,
                ordered=False,
            )
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


def category(request):
    categories = Category.objects.filter(active=True,)
    context = {
        'categories': categories
    }
    return render(request, 'pages/category.html', context)


def productDetails(request, slug):
    quantityForm = QuantityForm(request.POST)
    products = Product.objects.filter(
        slug=slug, active=True,)
    date = datetime.datetime.now().hour
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.filter(user=request.user,ordered=False)
    
    cartItem = CartItems.objects.values()
    
        
    
    product_data = Product.objects.get(slug=slug)
    
    totalOrderPricelist = []
    for totalPriceCheck in cartItem:
        totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    total = sum(totalOrderPricelist)

    context = {
        # 'product_id': products.id,
        # "name": products.name,
        # "category": products.category,
        # "price": products.price,
        # "description": products.description,
        # "stock": products.stock,
        # 'date': date,
        'form': quantityForm,
        'products': products
    }
    print(request.user)

    if request.method == 'POST':
        if quantityForm.is_valid():
            # print(products.price)

            totalOrderItemPrice = product_data.price * \
                quantityForm.cleaned_data['Quantity']

            # if productID == product_data.id and slug == context['slug']:
            print('Done')
            CartItems.objects.create(
                user=request.user,
                cart=cart,
                product=product_data,
                ordered=False,
                # order = order,
                quantity=quantityForm.cleaned_data['Quantity'],
                totalOrderItemPrice = totalOrderItemPrice
            )

            # OrderItem.objects.filter(user=request.user, ordered=False,).update(
            #     product=products,
            #     user=request.user,
            #     ordered=False,
            #     quantity=quantityForm.cleaned_data['Quantity'],
            #     totalOrderItemPrice=totalOrderItemPrice,
            # )

            # else:
            # print('Another_Product')
            # CartItems.objects.filter(user=request.user,ordered = False,).create(
            #     product=product_data,
            #     ordered=False,
            #     quantity=quantityForm.cleaned_data['Quantity'],
            #     totalOrderItemPrice=totalOrderItemPrice
            # )
            return redirect('checkout')

    return render(request, "pages/productDetails.html", context)


def cart(request):
    discountform = BromoCodeForm(
        request.POST, use_required_attribute=False,)
    products = Product.objects.filter(active=True,).values()
    bromocode = BromoCode.objects.filter(active=True,).values()
    categories = Category.objects.filter(active=True)
    userLoggedIN = Profile.objects.filter(username=request.user).first()
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

    return render(request, 'home/cart.html', context)


def store(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(active=True, category="1")
        categories = Category.objects.filter(active=True)
        userLoggedIN = Profile.objects.filter(username=request.user).first()
        if request.method == 'GET':

            if request.GET.get('search'):
                print('1'*50)
                search_products = products.filter(
                    name__icontains=request.GET.get('search'))

            if request.GET.get('level_select') != 'all' and request.GET.get('level_select'):
                search_products = search_products.filter(
                    level=request.GET.get('level_select'))
        context = {
            "products": products,
            "categories": categories,
            'userLoggedIN': userLoggedIN,
            # 'search_products' : search_products
        }
        return render(request, 'home/store.html', context)
    else:
        return redirect('sign')


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


class TestingAPI(APIView):

    def get(self, request):
        profile = Product.objects.all()
        serializers = Profileserializers(profile, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = Profileserializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


def checkout(request):
    discountform = BromoCodeForm(
        request.POST)
    userProfile = Profile.objects.filter(username=request.user).first()
    products = Product.objects.filter(active=True,).values()
    bromocode = BromoCode.objects.filter(active=True,).values()
    categories = Category.objects.filter(active=True)
    userLoggedIN = Profile.objects.filter(username=request.user).first()
    cartItem = CartItems.objects.filter(
        user=request.user, ordered=False).values()
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
        'total' : total,
        'userProfile' : userProfile   
    }
    cart = Cart.objects.get()
    if request.method == 'POST':
        total = total * sytax['percentage']
        context['total'] = total
        Order.objects.create(
            user=request.user,
            totalPrice=total,
            coupon = 'H',
            cart = cart,
        )
        CartItems.objects.update(
            ordered=True,
        )
        return redirect('ThankYou')
    return render(request, 'pages/checkout.html',context)



def ThankYou(request):
    return render(request, 'pages/thankyou.html')