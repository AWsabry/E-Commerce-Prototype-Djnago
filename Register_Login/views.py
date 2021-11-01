from rest_framework.response import Response
from Register_Login.models import BromoCode, Category, Order, OrderItem, Product, Profile
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


def product_detail(request, slug):
    quantityForm = QuantityForm(request.POST)
    products = Product.objects.filter(
        slug=slug, active=True,).first()
    date = datetime.datetime.now().hour
    user = Profile.objects.filter(username=request.user).first()
    order_item = OrderItem.objects.filter(
        user=request.user, ordered=False,).values()

    productID = ''
    for orderItem in OrderItem.objects.filter(user=request.user,ordered = False).values():
        productID = orderItem['product_id']

    user_ID = ''
    for userID in OrderItem.objects.filter(user=request.user).values():
        user_ID = userID['id']
    print(OrderItem.objects.all().values())

    context = {
        'product_id': products.id,
        "name": products.name,
        "category": products.category,
        "price": products.price,
        "description": products.description,
        "stock": products.stock,
        'date': date,
        'form': quantityForm,
        'slug': products.slug,
    }
    x = OrderItem.objects.filter(user=request.user).values('id')
    print(x)

    if request.method == 'POST':
        if quantityForm.is_valid():
            totalOrderItemPrice = products.price * \
                quantityForm.cleaned_data['Quantity']

            if productID == context['product_id'] and slug == context['slug']:
                print(context['product_id'])
                print('Done')

                OrderItem.objects.filter(user=request.user, ordered=False,).update(
                    product=products,
                    user=request.user,
                    ordered=False,
                    quantity=quantityForm.cleaned_data['Quantity'],
                    totalOrderItemPrice=totalOrderItemPrice,
                )

            else:
                print('Another_Product')
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
        user=request.user, ordered=False).values()

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

        OrderItem.objects.filter(
            user=request.user, ordered=False).update(ordered=True,)

        return redirect('done')

    return render(request, 'home/cart.html', context)


# def create_order(request):
#     cart=Cart(request)
#     order=models.Order(user=request.user)
#     data=models.OrderItem()
#     for x in cart.cart:
#         data.create(orders=order,product=x['product'],price=item['price'],quantity=item['quantity'],order_arrive_time = item['order_arrive_time'],order_code = item["order_code"])
#     cart.clear()
#     order.save()
#     #request.session['order_id'] = order.id
#     return HttpResponse('DONES')


def done(request):
    return render(request, 'home/done.html')
    

def store(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)
        userLoggedIN = Profile.objects.filter(username=request.user).first()
        context = {
            "products": products,
            "categories": categories,
            'userLoggedIN': userLoggedIN,
        }
        return render(request, 'home/store.html',context)
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
