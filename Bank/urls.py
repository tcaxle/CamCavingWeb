from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('Create/Entry/', views.CreateEntry.as_view(), name='CreateEntry'),
    path('Edit/Entry/<slug:slug>', views.EditEntry.as_view(), name='EditEntry'),
    path('View/Account/<slug:slug>', views.ViewAccount.as_view(), name='ViewAccount'),
    path('List/Accounts/', views.ListAccounts.as_view(), name='ListAccounts'),

    path('ToggleApprove/Entry/<slug:slug>', views.ToggleApproveEntry, name='ToggleApproveEntry'),
    path('ToggleApprove/Trnsaction/<slug:slug>', views.ToggleApproveTransaction, name='ToggleApproveTransaction'),
    path('ToggleApprove/TransactionGroup/<slug:slug>', views.ToggleApproveTransactionGroup, name='ToggleApproveTransactionGroup'),

    path('View/Entry/<slug:slug>', views.ViewEntry.as_view(), name='ViewEntry'),
    path('View/Transaction/<slug:slug>', views.ViewTransaction.as_view(), name='ViewTransaction'),
    path('View/TransactionGroup/<slug:slug>', views.ViewTransactionGroup.as_view(), name='ViewTransactionGroup'),

    path('Delete/Entry/<slug:slug>', views.DeleteEntry.as_view(), name='DeleteEntry'),
    path('Delete/Transaction/<slug:slug>', views.DeleteTransaction.as_view(), name='DeleteTransaction'),
    path('Delete/TransactionGroup/<slug:slug>', views.DeleteTransactionGroup.as_view(), name='DeleteTransactionGroup'),

    path('Create/Account/', views.CreateAccount.as_view(), name='CreateAccount'),

    path('Create/Transaction/Creditor/', views.CreateTransactionCreditor.as_view(), name='CreateTransactionCreditor'),
    path('Create/Transaction/Debtor/', views.CreateTransactionDebtor.as_view(), name='CreateTransactionDebtor'),
    path('Create/Transaction/Data/', views.CreateTransactionData.as_view(), name='CreateTransactionData'),
    path('Create/Transaction/', RedirectView.as_view(url='Creditor/'), name='CreateTransaction'),
    path('Redirect/Create/Transaction/', views.CreateTransactionAction, name='CreateTransactionAction'),

    path('Edit/Transaction/Creditor/<slug:slug>', views.EditTransactionCreditor.as_view(), name='EditTransactionCreditor'),
    path('Edit/Transaction/Debtor/<slug:slug>', views.EditTransactionDebtor.as_view(), name='EditTransactionDebtor'),
    path('Edit/Transaction/Data/<slug:slug>', views.EditTransactionData.as_view(), name='EditTransactionData'),
    path('Redirect/Edit/Transaction/', views.EditTransactionAction, name='EditTransactionAction'),

    path('Create/TransactionGroup/Creditor/', views.CreateTransactionGroupCreditor.as_view(), name='CreateTransactionGroupCreditor'),
    path('Create/TransactionGroup/Debtor/', views.CreateTransactionGroupDebtor.as_view(), name='CreateTransactionGroupDebtor'),
    path('Create/TransactionGroup/Data/', views.CreateTransactionGroupData.as_view(), name='CreateTransactionGroupData'),
    path('Create/TransactionGroup/', RedirectView.as_view(url='Creditor/'), name='CreateTransactionGroup'),
    path('Redirect/Create/TransactionGroup/', views.CreateTransactionGroupAction, name='CreateTransactionGroupAction'),

    path('Edit/TransactionGroup/Creditor/<slug:slug>', views.EditTransactionGroupCreditor.as_view(), name='EditTransactionGroupCreditor'),
    path('Edit/TransactionGroup/Debtor/<slug:slug>', views.EditTransactionGroupDebtor.as_view(), name='EditTransactionGroupDebtor'),
    path('Edit/TransactionGroup/Data/<slug:slug>', views.EditTransactionGroupData.as_view(), name='EditTransactionGroupData'),
    path('Redirect/Edit/TransactionGroup/', views.EditTransactionGroupAction, name='EditTransactionGroupAction'),

]
