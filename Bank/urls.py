from django.urls import path
from . import views

urlpatterns = [
    path('Create/Entry/', views.CreateEntry.as_view(), name='CreateEntry'),
    path('Create/Account/', views.CreateAccount.as_view(), name='CreateAccount'),
    path('Create/Transaction/Creditor/', views.CreateTransactionCreditor.as_view(), name='CreateTransactionCreditor'),
    path('Create/Transaction/Debtor/', views.CreateTransactionDebtor.as_view(), name='CreateTransactionDebtor'),
    path('Create/Transaction/Data/', views.CreateTransactionData.as_view(), name='CreateTransactionData'),
    path('Redirect/Create/Transaction/', views.CreateTransactionAction, name='CreateTransactionAction')
]
