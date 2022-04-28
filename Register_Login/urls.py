from django.urls import path
from django.contrib.auth import views
from Register_Login.views import Register, logOut, signIn,email_sent,activate_user


app_name = 'Register_Login'

urlpatterns = [
    path('Register', view = Register, name='Register'),
    path('sign', view = signIn, name='sign'),
    path('logOut',view = logOut, name='logOut'),
    path(route='activate/<token>', view= activate_user, name='activate'),
    path('email_sent', view = email_sent, name='email_sent'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
