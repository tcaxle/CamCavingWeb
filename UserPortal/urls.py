# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('SignUp/', views.SignUp.as_view(), name='SignUp'),
    path('EditProfile/<slug:slug>/', views.EditProfile.as_view(), name='EditProfile'),
    path('SuperEditProfile/<slug:slug>/', views.SuperEditProfile.as_view(), name='SuperEditProfile'),
    path('Password/', views.ChangePassword, name='ChangePassword'),
    path('Dashboard/', views.UserPortalDashboard.as_view(), name='UserPortalDashboard'),
    path('EditUsers/', views.EditUsers.as_view(), name='EditUsers'),
    path('CommitteeAdd/', views.CommitteeAdd.as_view(), name='CommitteeAdd'),
    path('CommitteeEdit/<int:pk>', views.CommitteeEdit.as_view(), name='CommitteeEdit'),
    path('CommitteeDelete/<int:pk>', views.CommitteeDelete.as_view(), name='CommitteeDelete'),
    path('RankAdd/', views.RankAdd.as_view(), name='RankAdd'),
    path('RankEdit/<int:pk>', views.RankEdit.as_view(), name='RankEdit'),
    path('RankDelete/<int:pk>', views.RankDelete.as_view(), name='RankDelete'),
]
