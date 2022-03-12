from django.http.response import HttpResponse
from rest_framework.response import Response
from Register_Login.models import AccessToken, Profile
from Register_Login.forms import CompleteProfile, LoginForm, RegisterForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as user_login
from rest_framework.views import APIView
from rest_framework import status
from Register_Login.serializers import Profileserializers
from django.template.loader import render_to_string
from django.utils import timezone
from Ecommerce_prototype import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage

from Register_Login.utils import AccessTokenGenerator
from cart_and_orders.models import Cart
from categories_and_products.models import Product


# Email Confirm SignUp
def send_tracking(user):
    user = Profile.objects.filter(id=user.id).first()
    last_token = user.token.filter(
        user=user, expires__gt=timezone.now()).first()
    if not last_token:
        access_token = user.token.create(user=user)
        return (access_token.token, 0)
    return (False, (last_token.expires - timezone.now()).total_seconds())


def token_check(user):
    token, time_tosend = send_tracking(user=user)
    if token:
        Cart.objects.create(
                    user=user,
                    ordered=False,
                )
        return (token, time_tosend)
    return (None, time_tosend)


def send_activate_mail(request, user):
    token, time_tosend = token_check(user)
    if token:
        print(token)
        domain = get_current_site(request)
        subject = _('Activate user account')
        body = render_to_string('activate.html', {
            'user': user,
            'domain': domain,
            'token': token,
        })
        email = EmailMessage(
            subject, body, settings.EMAIL_HOST_USER, [user.email])
        print(email)
        email.send()
       
        messages.success(request, _('There are an mail has been sent.'))
    else:
        messages.error(request, _('Please varify the account (an email have been sent) please wait %(time_tosend)8.0f') % {
                       'time_tosend': time_tosend}, extra_tags='danger')


@csrf_exempt
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = form.data.get('email')
        first_name, last_name = form.data.get(
            'first_name'), form.data.get('last_name')
        password = form.data.get('password1')
        # if form.is_valid():
        user = Profile.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,)

        # print("Done_02")
        send_activate_mail(request, user)
        # print("Done_03")
        # print(email)
        # Cart.objects.create(
        #         user=users ,
        #         ordered=False,
        #     )
        return redirect('email_sent')
        # else:
        #     messages.error(request, _(
        #         'This showing something wrong!'), extra_tags='danger')
    else:
        form = RegisterForm()
    # form = RegisterForm(request.POST, request.FILES)
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:
    #     if request.method == 'POST':
    #         print("Done_01")
    #         if form.is_valid():
    #             print("Done_02")
    #             user = form.save()
    #             login(request, user)
    #             print("Done_03")
    #             return redirect('index')
        return render(request, "Register.html",  {
            # 'form': form
        })


def activate_user(request, token):
    token = AccessToken.objects.filter(token=token).first()
    if token:
        last_token = AccessToken.objects.filter(
            user=token.user, expires__gt=timezone.now()).first()

        if last_token == token:
            if AccessTokenGenerator().check_token(token.user, token.token):
                token.user.is_active = True
                token.user.save()
                return HttpResponse('activated')
            return HttpResponse('already activated')
        return HttpResponse('timeout')

    return HttpResponse('None found token')


def email_sent(request):
    return render(request,"email_sent.html")

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
    return render(request, "completeProfile.html",  {
        'form': form,
    })


def logOut(request):
    logout(request)
    form = LoginForm(request.POST, request.FILES)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'signIn.html',{'form': form})


def sign(request):
    form = LoginForm(request.POST, request.FILES)
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            if form.is_valid():
                print("Post")

                email = request.POST.get('email')
                password = request.POST.get('password')
                user = authenticate(request, email=email, password=password)
                user_login(request, user)
                return redirect('index')
        return render(request, 'signIn.html', {'form': form})


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
