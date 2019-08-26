from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('Create/Entry/', views.CreateEntry.as_view(), name='CreateEntry'),
    path('Create/Account/', views.CreateAccount.as_view(), name='CreateAccount'),
    
    path('Create/Transaction/Creditor/', views.CreateTransactionCreditor.as_view(), name='CreateTransactionCreditor'),
    path('Create/Transaction/Debtor/', views.CreateTransactionDebtor.as_view(), name='CreateTransactionDebtor'),
    path('Create/Transaction/Data/', views.CreateTransactionData.as_view(), name='CreateTransactionData'),
    path('Create/Transaction/', RedirectView.as_view(url='Creditor/'), name='CreateTransaction'),
    path('Redirect/Create/Transaction/', views.CreateTransactionAction, name='CreateTransactionAction'),

    path('Create/TransactionGroup/Creditor/', views.CreateTransactionGroupCreditor.as_view(), name='CreateTransactionGroupCreditor'),
    path('Create/TransactionGroup/Debtor/', views.CreateTransactionGroupDebtor.as_view(), name='CreateTransactionGroupDebtor'),
    path('Create/TransactionGroup/Data/', views.CreateTransactionGroupData.as_view(), name='CreateTransactionGroupData'),
    path('Create/TransactionGroup/', RedirectView.as_view(url='Creditor/'), name='CreateTransactionGroup'),
    path('Redirect/Create/TransactionGroup/', views.CreateTransactionGroupAction, name='CreateTransactionGroupAction')
]
