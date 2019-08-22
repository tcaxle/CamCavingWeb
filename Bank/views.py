from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.utils import timezone
from .models import *
from .forms import *
from UserPortal.models import CustomUser

def TransactionsToDate(account, date=timezone.now()):
    return account.transaction_set.filter(date__lte=date).order_by('-date')

def BalanceAtDate(account, date=timezone.now()):
    return account.transaction_set.filter(date__lte=date).aggregate(Sum('amount'))

class ViewAccount(DetailView):
    model = Account
    template_name = 'Bank/ViewAccount.html'
    slug_field = 'account_key'
    context_object_name = 'account'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_date = timezone.now()
        context['transaction_list'] = TransactionsToDate(context['account'], view_date)
        context['balance'] = BalanceAtDate(context['account'], view_date)
        return context

class ListAccounts(ListView):
    model = Account
    template_name = 'Bank/ListAccounts.html'
    context_object_name = 'accounts_list'

class AddTransaction(CreateView):
    model = Transaction
    form_class = AddTransaction
    template_name = 'Bank/AddTransaction.html'
    success_url = reverse_lazy('UserPortalDashboard')

class SuperAddTransaction(CreateView):
    model = Transaction
    form_class = SuperAddTransaction
    template_name = 'Bank/AddTransaction.html'
