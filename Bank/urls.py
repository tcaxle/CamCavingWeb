from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('Create/Entry/', views.CreateEntry.as_view(), name='CreateEntry'),
    path('Edit/Entry/<slug:slug>', views.EditEntry.as_view(), name='EditEntry'),
    path('View/Account/<slug:slug>', views.ViewAccount.as_view(), name='ViewAccount'),
    path('List/Accounts/', views.ListAccounts.as_view(), name='ListAccounts'),

    path('View/Entry/<slug:slug>', views.ViewEntry.as_view(), name='ViewEntry'),
    path('View/Transaction/<slug:slug>', views.ViewTransaction.as_view(), name='ViewTransaction'),
    path('View/TransactionGroup/<slug:slug>', views.ViewTransactionGroup.as_view(), name='ViewTransactionGroup'),

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
