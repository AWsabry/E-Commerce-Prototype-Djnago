import imp
from django.urls import path, include
from django.contrib.auth import views

from Register_Login.views import Register, completeProfile, logOut, sign,email_sent,activate_user,TestingAPI


urlpatterns = [
    path('Register', view = Register, name='Register'),
    path('sign', view = sign, name='sign'),
    path('logOut',view = logOut, name='logOut'),
    path('completeProfile', view = completeProfile, name='completeProfile',),
    path(route='activate/<token>', view= activate_user, name='activate'),
    path('email_sent', view = email_sent, name='email_sent'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),




    path('test', view = TestingAPI.as_view(), name='testingapi')
]
