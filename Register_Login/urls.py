from django.urls import path
from . import views


urlpatterns = [
    path('Register',views.Register,name='Register'),
    path('signIn',views.signIn, name='signin'),
    path('logOut',views.logOut,name='logOut'),
    path('completeProfile',views.completeProfile,name='completeProfile',),
    path('',views.index,name='index',),
    path('<slug:slug>',views.product_detail,name='product_detail'),
]