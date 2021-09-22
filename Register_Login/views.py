from Register_Login.models import Category, Product, RegisterationModel
from Register_Login.forms import CompleteProfile, LoginForm, RegisterForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def completeProfile(request):
    if request.method == 'POST':
        form = CompleteProfile(request.POST, request.FILES)
        if form.is_valid():
            form.instance.username = request.user
            context = {}
            context['form'] = form
            form.save()
            return render(request, 'home/done.html', {'form': form})
    else:
        form = CompleteProfile()
    return render(request, "home/completeProfile.html",  {
        'form': form,
    })


def Register(request):
    if request.user.is_authenticated:
        return render(request, "home/done.html")
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                print(user)
                login(request, user)
                print("HI")
                messages.success(request, "Registration successful.")
                return render(request, "home/completeProfile.html", {'form': form})
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


def signIn(request):
    if request.user.is_authenticated:
        return render(request, "home/done.html")
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

                    return render(request, "home/done.html")
                else:
                    messages.error(request, "Invalid username or password.")
                    return render(request, "home/signIn.html", {'form': form})
        else:
            form = LoginForm()
        return render(request, 'home/signIn.html', {'form': form})


def done(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'home/done.html')


def index(request):
    return render(request, 'home/index.html')


@login_required
def index(request):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    userLoggedIN = RegisterationModel.objects.filter(username=request.user).first()

    context = {
        "products": products, 
        "categories": categories, 
        'userLoggedIN': userLoggedIN ,
    }
    return render(request, 'home/index.html', context)

def product_detail(request,id):
    products = Product.objects.get(pk=id)
    return render(request, "home/product_detail.html",{
        "name": products.name,
        "category": products.category,
        "price": products.price,
        "description": products.description,
        "stock": products.stock,

    })