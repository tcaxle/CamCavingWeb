from django.urls import path
from . import views

urlpatterns = [
    path('Create/Entry/', views.CreateEntry.as_view(), name='CreateEntry'),
    path('Create/Account/', views.CreateAccount.as_view(), name='CreateAccount'),
    path('Create/Transaction/', views.CreateTransaction.as_view(), name='CreateTransaction'),
    path('Redirect/Create/Transaction/', views.CreateTransactionAction, name='CreateTransactionAction')
]
