from django.urls import path,include

from . import views


urlpatterns = [
    path('',views.index,name='index',),
    path('category',views.category,name='category'),
    path('store',views.store,name='store'),
    path('product/<slug:slug>',views.productDetails,name='productDetails'),


    path('laptops', views.laptops, name='laptops'),
    path('smartphones', views.smartphones, name='smartphones'),
    path('cameras', views.cameras, name='cameras'),
    path('accessories', views.accessories, name='accessories'),


    path('filter',views.filtering_test,name='filter'),



]