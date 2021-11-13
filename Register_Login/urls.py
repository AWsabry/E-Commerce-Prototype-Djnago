from django.urls import path,include
from . import views


urlpatterns = [
    path('Register',views.Register,name='Register'),
    path('sign',views.sign, name='sign'),
    path('logOut',views.logOut,name='logOut'),
    path('completeProfile',views.completeProfile,name='completeProfile',),
    path('',views.index,name='index',),
    path('<slug:slug>/',views.productDetails,name='productDetails'),
    path('cart',views.cart,name='cart'),
    path('category/',views.category,name='category'),
    path('store',views.store,name='store'),
    path('checkout',views.checkout,name='checkout'),


    path('test',views.TestingAPI.as_view(),name = 'testingapi')
]