from django.urls import path,include
from . import views


urlpatterns = [
    path('Register',views.Register,name='Register'),
    path('sign',views.sign, name='sign'),
    path('logOut',views.logOut,name='logOut'),
    path('completeProfile',views.completeProfile,name='completeProfile',),
    path('',views.index,name='index',),
    path('<slug:slug>/',views.product_detail,name='product_detail'),
    path('cart',views.cart,name='cart'),
    path('done',views.done,name='done'),
    path('store',views.store,name='store'),


    path('test',views.TestingAPI.as_view(),name = 'testingapi')
]