from django.shortcuts import render, redirect
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
from django.shortcuts import get_object_or_404
from django.http import Http404

class CreateEntry(FormView):
    form_class = CreateEntry
    template_name = 'Bank/AddEntry.html'
    success_url = reverse_lazy('CreateEntry')

    def form_valid(self, form):
        from_account = form.cleaned_data['creditor']
        to_account = form.cleaned_data['debtor']
        amount = form.cleaned_data['amount']
        date = form.cleaned_data['date']
        notes = form.cleaned_data['notes']
        entry = Entry.create(from_account, to_account, amount, date, notes)
        entry.save()
        return super().form_valid(form)

class CreateAccount(CreateView):
    model = Account
    template_name = 'Bank/AddAccount.html'
    fields = '__all__'
    success_url = reverse_lazy('CreateAccount')

class ViewAccount(DetailView):
    # Returns a transaction list with date filtering options for an account
    pass

class ViewTransactions(ListView):
    # Returns a transaction list with date filtering options for all accounts
    pass


class CreateExpense(FormView):
    # Allows users to create pending transactions to claim expenses
    pass

class CreateOneToOneSwap(FormView):
    # Allows users to create person to person swaps
    pass

class CreateManyToOneSwap(FormView):
    # Allows users to create many to one swaps (splits)
    pass

class CreateManyToManySwap(FormView):
    # Allows users to create many to one swaps (splits)
    pass

class CreateMeetAccounts(FormView):
    # Allows users to easily record a meet's accounts
    # Create's prending transactions for each member on the trip
    pass

class ReviewTransaction(DetailView):
    # Allows the treasurer to review a pendig transaction
    # and to migrate it to a book transaction, or two books and a bank tranaction
    pass

class CreateTransactionCreditor(TemplateView):
    # Allows the treasurer to create transactions
    template_name = 'Bank/AddTransaction/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

class CreateTransactionDebtor(TemplateView):
    # Allows the treasurer to create transactions
    template_name = 'Bank/AddTransaction/SelectDebtor.html'
    def post(self, request, *args, **kwargs):
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        # Banks and Pools CANNOT transact:
        if creditor.type == 'Bank':
            account_list = Account.objects.exclude(type='Pool').order_by('name')
        elif creditor.type == 'Pool':
            account_list = Account.objects.exclude(type='Bank').order_by('name')
        else:
            account_list = Account.objects.all().order_by('name')
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

class CreateTransactionData(TemplateView):
    template_name = 'Bank/AddTransaction/InputData.html'
    def post(self, request, *args, **kwargs):
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        all_accounts = Account.objects.all()
        account_list = Account.objects.none()
        for account in all_accounts:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'TRUE':
                account_list = account_list.union(all_accounts.filter(account_key=key))
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

def CreateTransactionAction(request):
    if request.method == 'POST':
        transaction = Transaction()
        transaction.save()
        data = request.POST
        account_list = Account.objects.all()
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        notes = data.get('notes')
        for account in account_list:
            key = str(account.account_key)
            if key in data.keys() and data.get(key):
                debtor = account
                amount = data.get(key)
                entry = Entry.create(account_a=creditor, account_b=debtor, credit_a=float(amount), date=date, notes=notes)
                entry.save()
                transaction.entry_set.add(entry) # Create and add each entry to the object
        transaction.save()
    return redirect('CreateTransactionCreditor')

class EditTransaction(TemplateView):
    # Allos the treasurer to edit transactions
    pass

class DeleteTransaction(DeleteView):
    # Allows the treasurer to delete transactions
    pass
