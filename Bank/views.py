from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .forms import *
from UserPortal.models import CustomUser

def TransactionsToDate(account, date=timezone.now()):
    # Returns a query set of all transactions up to a date on an account
    return account.transaction_set.filter(date__lte=date)

def BalanceAtDate(account, date=timezone.now()):
    # Returns the balance as a float
    balance = account.transaction_set.filter(date__lte=date).aggregate(Sum('amount')).get('amount__sum')
    if balance == None:
        return float(0.00)
    else:
        return float(balance)

def BalanceList(transaction_list):
    # takes a list of transaction objects, and returns a dictionary of {transaction: balance}
    balance_list = []
    for transaction in transaction_list:
        balance_list.append(BalanceAtDate(transaction.account, transaction.date))
    return dict(zip(transaction_list, balance_list))

class ViewAccount(DetailView):
    model = Account
    template_name = 'Bank/ViewAccount.html'
    slug_field = 'account_key'
    context_object_name = 'account'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = context['account']
        if self.request.method == 'GET':
            if 'end_date' in self.request.GET and self.request.GET['end_date']:
                start_date = datetime.strptime(self.request.GET['start_date'], '%Y-%m-%d')
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                context['view_earliest'] = False
            else:
                start_date = account.transaction_set.order_by('date')[0].date
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                context['view_earliest'] = True
            context['start_date'] = start_date
            if 'end_date' in self.request.GET and self.request.GET['end_date']:
                end_date = datetime.strptime(self.request.GET['end_date'], '%Y-%m-%d')
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 5)
                context['view_latest'] = False
            else:
                end_date = datetime.now()
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 5)
                context['view_latest'] = True
            context['end_date'] = end_date
            context['start_balance'] = BalanceAtDate(account, start_date)
            context['end_balance'] = BalanceAtDate(account, end_date)
            context['balance_list'] = BalanceList(list(TransactionsToDate(account, end_date).difference(TransactionsToDate(account, start_date)).order_by('-date')))
        return context

class ViewOwnAccount(TemplateView):
    template_name = 'Bank/ViewAccount.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.request.user.bank_account
        context['account'] = account
        start_date = account.transaction_set.order_by('date')[0].date
        start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
        context['view_earliest'] = True
        context['start_date'] = start_date
        end_date = datetime.now()
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 5)
        context['view_latest'] = True
        context['end_date'] = end_date
        context['start_balance'] = BalanceAtDate(account, start_date)
        context['end_balance'] = BalanceAtDate(account, end_date)
        context['balance_list'] = BalanceList(list(TransactionsToDate(account, end_date).difference(TransactionsToDate(account, start_date)).order_by('-date')))
        return context

class ListTransactions(ListView):
    model = Transaction
    template_name = 'Bank/ListTransactions.html'
    context_object_name = 'transaction_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_list = context['transaction_list']
        if self.request.method == 'GET':
            if 'start_date' in self.request.GET and self.request.GET['start_date']:
                start_date = datetime.strptime(self.request.GET['start_date'], '%Y-%m-%d')
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                context['view_earliest'] = False
            else:
                start_date = transaction_list.order_by('date')[0].date
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                context['view_earliest'] = True
            context['start_date'] = start_date
            if 'end_date' in self.request.GET and self.request.GET['end_date']:
                end_date = datetime.strptime(self.request.GET['end_date'], '%Y-%m-%d')
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 5)
                context['view_latest'] = False
            else:
                end_date = datetime.now()
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 5)
                context['view_latest'] = True
            context['end_date'] = end_date
        else:
            start_date = transaction_list.order_by('date')[0].date
            start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            context['view_earliest'] = True
            context['start_date'] = start_date
            end_date = datetime.now()
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 5)
            context['view_latest'] = True
            context['end_date'] = end_date
        return context

class ListAccounts(ListView):
    model = Account
    template_name = 'Bank/ListAccounts.html'
    context_object_name = 'accounts_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts_list = context['accounts_list']
        balance_list = []
        for account in accounts_list:
            balance_list.append(BalanceAtDate(account))
        context['account_dict'] = dict(zip(accounts_list, balance_list))
        return context

class AddTransaction(CreateView):
    model = Transaction
    form_class = AddTransaction
    template_name = 'Bank/AddTransaction.html'
    success_url = reverse_lazy('ViewOwnAccount')

class AddTransactionPair(FormView):
    form_class = AddTransactionPair
    template_name = 'Bank/AddTransaction.html'
    success_url = reverse_lazy('ViewOwnAccount')
    def form_valid(self, form):
        account_a = form.cleaned_data['from_account']
        account_b = form.cleaned_data['to_account']
        date = form.cleaned_data['date']
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions take place at Mid-Day so that when you are viewing transactions for a single day, you get all of them
        amount = form.cleaned_data['amount']
        category = form.cleaned_data['category']
        notes = form.cleaned_data['notes']
        transaction_pair = TransactionPair.create(account_a, account_b, date, amount, category, notes)
        transaction_pair.transaction_a.save()
        transaction_pair.transaction_b.save()
        transaction_pair.save()
        return super().form_valid(form)

class SuperAddTransactionPair(FormView):
    form_class = SuperAddTransactionPair
    template_name = 'Bank/AddTransaction.html'
    success_url = reverse_lazy('ViewOwnAccount')
    def form_valid(self, form):
        account_a = form.cleaned_data['from_account']
        account_b = form.cleaned_data['to_account']
        date = form.cleaned_data['date']
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions take place at Mid-Day so that when you are viewing transactions for a single day, you get all of them
        amount = form.cleaned_data['amount']
        category = form.cleaned_data['category']
        notes = form.cleaned_data['notes']
        approved = form.cleaned_data['approved']
        transaction_pair = TransactionPair.create(account_a, account_b, date, amount, category, notes)
        transaction_pair.transaction_a.save()
        transaction_pair.transaction_b.save()
        transaction_pair.save()
        return super().form_valid(form)


class SuperAddTransaction(CreateView):
    model = Transaction
    form_class = SuperAddTransaction
    template_name = 'Bank/AddTransaction.html'
