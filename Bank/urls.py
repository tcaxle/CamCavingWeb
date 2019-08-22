from django.urls import path
from . import views

urlpatterns = [
    path('ViewAccount/<slug:slug>/', views.ViewAccount.as_view(), name='ViewAccount'),
    path('ListAccounts/', views.ListAccounts.as_view(), name='ListAccounts'),
    path('Transaction/Add/', views.AddTransaction.as_view(), name='AddTransaction'),
    path('Transaction/SuperAdd/', views.SuperAddTransaction.as_view(), name='SuperAddTransaction'),
]
