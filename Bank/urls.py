from django.urls import path
from . import views

urlpatterns = [
    path('ListAccounts/', views.ListAccounts.as_view(), name='ListAccounts'),
    path('ViewAccount/', views.ViewOwnAccount.as_view(), name='ViewOwnAccount'),
    path('ViewAccount/<slug:slug>/', views.ViewAccount.as_view(), name='ViewAccount'),
    path('Transaction/Add/', views.AddTransaction.as_view(), name='AddTransaction'),
    path('Transaction/SuperAdd/', views.SuperAddTransaction.as_view(), name='SuperAddTransaction'),
    path('TransactionPair/Add/', views.AddTransactionPair.as_view(), name='AddTransactionPair'),
    path('TransactionPair/SuperAdd/', views.SuperAddTransactionPair.as_view(), name='SuperAddTransactionPair'),
    path('ListTransactions/', views.ListTransactions.as_view(), name='ListTransactions'),
]
