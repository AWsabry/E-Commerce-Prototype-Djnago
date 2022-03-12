from django.shortcuts import redirect, render
from Register_Login.models import Profile
from cart_and_orders.models import Cart, CartItems, Order
from categories_and_products.forms import QuantityForm
from categories_and_products.models import Category, Product
from django.core.paginator import Paginator

import datetime


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)
        userLoggedIN = Profile.objects.filter(id=request.user.id).first()

        context = {
            "products": products,
            "categories": categories,
            'userLoggedIN': userLoggedIN,
        }
        return render(request, 'index.html', context)
    else:
        return redirect('sign')


def category(request):
    categories = Category.objects.filter(active=True,)
    context = {
        'categories': categories
    }
    return render(request, 'category.html', context)


def store(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(active=True,)
        categories = Category.objects.filter(active=True)
        userLoggedIN = Profile.objects.filter(id=request.user.id).first()
        if request.method == 'GET':

            if request.GET.get('search'):
                print('1'*50)
                search_products = products.filter(
                    name__icontains=request.GET.get('search'))

            if request.GET.get('level_select') != 'all' and request.GET.get('level_select'):
                search_products = search_products.filter(
                    level=request.GET.get('level_select'))

        page = request.GET.get('page')
        p_obj = Paginator(products.order_by('-created'), 1)
        context = {
            "products": products,
            "categories": categories,
            'userLoggedIN': userLoggedIN,
            'p_obj' : p_obj.get_page(1)
            # 'search_products' : search_products
        }

     

        return render(request, 'store.html', context)
    else:
        return redirect('Register_Login:sign')




def laptops(request):
    products = Product.objects.filter(active=True,category__name='laptop')
    categories = Category.objects.filter(active=True)
    context = {
            "products": products,
            "categories": categories,
    }

    return render(request,'laptops.html', context)



def smartphones(request):
    products = Product.objects.filter(active=True,category__name='Mobile')
    categories = Category.objects.filter(active=True)
    context = {
            "products": products,
            "categories": categories,
    }

    return render(request,'smartphones.html', context)



def cameras(request):
    products = Product.objects.filter(active=True,category__name='cameras')
    categories = Category.objects.filter(active=True)
    context = {
            "products": products,
            "categories": categories,
    }

    return render(request,'cameras.html', context)


def accessories(request):
    products = Product.objects.filter(active=True,category__name='accessories')
    categories = Category.objects.filter(active=True)
    context = {
            "products": products,
            "categories": categories,
    }

    return render(request,'accessories.html', context)

def productDetails(request, slug):
    quantityForm = QuantityForm(request.POST)
    products = Product.objects.filter(
        slug=slug, active=True,)
    date = datetime.datetime.now().hour
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.filter(user=request.user, ordered=False)

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
                totalOrderItemPrice=totalOrderItemPrice
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
            return redirect('cart_and_orders:checkout')

    return render(request, "productDetails.html", context)


def filtering_test(request):
    products = Product.objects.filter(active=True,category ="").values()
    print(products)
    return render(request, 'filter.html', {'products': products})
