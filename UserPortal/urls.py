# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('SignUp/', views.SignUp.as_view(), name='SignUp'),
    path('Password/', views.ChangePassword, name='ChangePassword'),
]
