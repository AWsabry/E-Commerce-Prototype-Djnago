from Register_Login.models import Category, Product, Profile
from Register_Login.forms import CompleteProfile, LoginForm, RegisterForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def Register(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)
        context = {
            "products": products,
            "categories": categories,
        }
        return render(request, "home/index.html", context)
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            completeProfileForm = CompleteProfile(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                print(user)
                login(request, user)
                print("HI")
                return render(request, "home/completeProfile.html", {'form': completeProfileForm})
            else:
                print("TEST")
            form = RegisterForm()
            return render(request, "home/Register.html",  {
                'form': form
            })
        else:
            print("WHy")
            form = RegisterForm()
        return render(request, "home/Register.html",  {
            'form': form
        })


def completeProfile(request):
    if request.method == 'POST':
        form = CompleteProfile(request.POST, request.FILES)
        products = Product.objects.filter(active=True)
        categories = Category.objects.filter(active=True)

        if form.is_valid():
            form.instance.username = request.user
            context = {}
            context['form'] = form
            form.save()
            prodcut = {
                "products": products,
                "categories": categories,
            }
            return render(request, 'home/index.html', prodcut)
    else:
        form = CompleteProfile()
    return render(request, "home/completeProfile.html",  {
        'form': form,
    })


def signIn(request):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    context = {
            "products": products,
            "categories": categories,
        }
        
    if request.user.is_authenticated:
        return render(request, "home/index.html", context)
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST, request.FILES)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    print(user)
                    login(request, user)
                    messages.info(
                        request, f"You are now logged in as {username}.")

                    return render(request, "home/index.html",context)
                else:
                    messages.error(request, "Invalid username or password.")
                    return render(request, "home/signIn.html", {'form': form})
        else:
            form = LoginForm()
        return render(request, 'home/signIn.html', {'form': form})


def logOut(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'home/LogOut.html')


def index(request):
    form = LoginForm()
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
        return render(request, 'home/signIn.html', {'form': form})


@login_required
def product_detail(request, slug):
    products = Product.objects.get(slug=slug)
    return render(request, "home/product_detail.html", {
        "name": products.name,
        "category": products.category,
        "price": products.price,
        "description": products.description,
        "stock": products.stock,
    })
