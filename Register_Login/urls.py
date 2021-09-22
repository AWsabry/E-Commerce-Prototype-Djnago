from django.urls import path
from . import views


urlpatterns = [
    path('',views.Register,name='Register'),
    path('signin',views.signIn, name='signin'),
    path('done',views.done,name='done'),
    path('completeProfile',views.completeProfile,name='completeProfile',),
    path('index',views.index,name='index',),
    path('product_detail',views.product_detail,name='product_detail'),
]