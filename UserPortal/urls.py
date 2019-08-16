# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('SignUp/', views.SignUp.as_view(), name='SignUp'),
    path('EditProfile/<slug:slug>/', views.EditProfile.as_view(), name='EditProfile'),
    path('SuperEditProfile/<slug:slug>/', views.SuperEditProfile.as_view(), name='SuperEditProfile'),
    path('Password/', views.ChangePassword, name='ChangePassword'),
    path('Dashboard/', views.UserPortalDashboard, name='UserPortalDashboard'),
    path('EditUsers/', views.EditUsers, name='EditUsers'),
]
