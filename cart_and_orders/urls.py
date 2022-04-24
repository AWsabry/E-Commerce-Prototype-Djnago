from django.urls import path, include

from . import views

app_name = 'cart_and_orders'


urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('thankyou', views.ThankYou, name='thankyou'),
]
