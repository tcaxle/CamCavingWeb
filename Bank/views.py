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

def TransactionsToDate(account, date=timezone.now()):
    # Returns a query set of all transactions up to a date on an account
    return account.transaction_set.filter(date__lte=date)

def BalanceAtDate(account, date=timezone.now()):
    # Returns the balance of an account at a date as a float
    balance_a = account.transaction_set_a.filter(date__lt=date).aggregate(Sum('credit_a')).get('credit_a__sum')
    balance_b = account.transaction_set_b.filter(date__lt=date).aggregate(Sum('credit_b')).get('credit_b__sum')
    balance = 0.0
    if balance_a is not None:
        balance = float(balance_a)
    if balance_b is not None:
        balance += float(balance_b)
    if balance_a is None and balance_b is None:
        balance = 0.0
    if balance == None:
        return float(0.00)
    else:
        return float(balance)

class CreateEntry(FormView):
    form_class = CreateEntry
    template_name = 'Bank/AddEntry.html'
    success_url = reverse_lazy('UserPortalDashboard')
    def form_valid(self, form):
        from_account = form.cleaned_data['creditor']
        to_account = form.cleaned_data['debtor']
        amount = form.cleaned_data['amount']
        date = form.cleaned_data['date']
        notes = form.cleaned_data['notes']
        entry = Entry.create(from_account, to_account, amount, date, notes)
        entry.created_by = self.request.user
        entry.save()
        return super().form_valid(form)

class EditEntry(UpdateView):
    model = Entry
    template_name = 'Bank/EditEntry.html'
    slug_field = 'entry_key'
    success_url = reverse_lazy('UserPortalDashboard')
    fields = ['account_a', 'account_b', 'credit_a', 'date', 'notes']

class CreateAccount(CreateView):
    model = Account
    template_name = 'Bank/AddAccount.html'
    fields = '__all__'
    success_url = reverse_lazy('UserPortalDashboard')

class ViewAccount(DetailView):
    # Returns a entry list with date filtering options for an account
    model = Account
    template_name = 'Bank/ViewAccount.html'
    slug_field = 'account_key'
    context_object_name = 'account'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = context['account']
        entry_set = account.transaction_set_a.all().union(account.transaction_set_b.all())
        if self.request.method == 'GET':
            if 'start_date' in self.request.GET and self.request.GET['start_date']:
                start_date = datetime.strptime(self.request.GET['start_date'], '%Y-%m-%d')
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                context['view_earliest'] = False
            else:
                start_date = entry_set.order_by('-date')[0].date
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
            context['entry_set'] = account.transaction_set_a.filter(date__range=(start_date, end_date)).union(account.transaction_set_b.filter(date__range=(start_date, end_date))).order_by('date')
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

class ViewTransaction(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/ViewTransaction.html'

class ViewTransactionGroup(DetailView):
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/ViewTransactionGroup.html'

class ViewEntry(DetailView):
    model = Entry
    slug_field = 'entry_key'
    context_object_name = 'entry'
    template_name = 'Bank/ViewEntry.html'

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
            account_list = Account.objects.exclude(type='Pool').order_by('type')
        elif creditor.type == 'Pool':
            account_list = Account.objects.exclude(type='Bank').order_by('type')
        else:
            account_list = Account.objects.all().order_by('type')
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
        if not account_list.first(): # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list.order_by('type')
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

def CreateTransactionAction(request):
    if request.method == 'POST':
        transaction = Transaction()
        transaction.created_by = request.user
        transaction.save()
        data = request.POST
        account_list = Account.objects.all()
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        notes = data.get('notes')
        for account in account_list:
            key = str(account.account_key)
            if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                debtor = account
                amount = data.get(key)
                entry = Entry.create(account_a=creditor, account_b=debtor, credit_a=float(amount), date=date, notes=notes)
                entry.created_by = request.user
                entry.transaction = transaction
                entry.save()
    return redirect('UserPortalDashboard')

class EditTransactionCreditor(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/EditTransaction/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

class EditTransactionDebtor(DetailView):
    # Allows the treasurer to create transactions
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/EditTransaction/SelectDebtor.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        # Banks and Pools CANNOT transact:
        if creditor.type == 'Bank':
            account_list = Account.objects.exclude(type='Pool').order_by('type')
        elif creditor.type == 'Pool':
            account_list = Account.objects.exclude(type='Bank').order_by('type')
        else:
            account_list = Account.objects.all().order_by('type')
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        date = self.object.entry_set.first().date
        creditor = self.object.entry_set.first().account_a
        # Banks and Pools CANNOT transact:
        if creditor.type == 'Bank':
            account_list = Account.objects.exclude(type='Pool').order_by('type')
        elif creditor.type == 'Pool':
            account_list = Account.objects.exclude(type='Bank').order_by('type')
        else:
            account_list = Account.objects.all().order_by('type')
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

class EditTransactionData(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/EditTransaction/InputData.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        all_accounts = Account.objects.all()
        account_list = Account.objects.none()
        for account in all_accounts:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'TRUE':
                account_list = account_list.union(all_accounts.filter(account_key=key))
        if not account_list.first(): # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list.order_by('type')
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        date = self.object.entry_set.first().date
        creditor = self.object.entry_set.first().account_a
        account_list = Account.objects.none()
        for entry in self.object.entry_set.all():
            account_list = account_list.union(Account.objects.filter(account_key=entry.account_b.account_key))
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list.order_by('type')
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

def EditTransactionAction(request):
    if request.method == 'POST':
        data = request.POST
        transaction = get_object_or_404(Transaction, transaction_key=data.get('transaction'))
        for entry in transaction.entry_set.all():
            entry.delete() # remove all previous entries
        account_list = Account.objects.all()
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        notes = data.get('notes')
        for account in account_list: # rebuild entries
            key = str(account.account_key)
            if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                debtor = account
                amount = data.get(key)
                entry = Entry.create(account_a=creditor, account_b=debtor, credit_a=float(amount), date=date, notes=notes)
                entry.created_by = request.user
                entry.transaction = transaction
                entry.save()
    return redirect('UserPortalDashboard')


class CreateTransactionGroupCreditor(TemplateView):
    # Allows the treasurer to create transactions
    template_name = 'Bank/AddTransactionGroup/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

class CreateTransactionGroupDebtor(TemplateView):
    # Allows the treasurer to create transactions
    template_name = 'Bank/AddTransactionGroup/SelectDebtor.html'
    def post(self, request, *args, **kwargs):
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        account_list = Account.objects.all()
        creditor_list = Account.objects.none()
        for account in account_list:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'creditor':
                creditor_list = creditor_list.union(account_list.filter(account_key=key))
        if not creditor_list.first(): # Check for no debtors selected
            raise Http404('You must have creditors in your transaction.') # Complain
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list.order_by('type')
        context['creditor_list'] = creditor_list.order_by('type')
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

class CreateTransactionGroupData(TemplateView):
    template_name = 'Bank/AddTransactionGroup/InputData.html'
    def post(self, request, *args, **kwargs):
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        account_list = Account.objects.all()
        creditor_list = Account.objects.none()
        debtor_list = Account.objects.none()
        for account in account_list:
            key = account.account_key
            if 'CREDITOR:'+str(key) in data.keys() and data.get('CREDITOR:'+str(key)) == 'creditor':
                creditor_list = creditor_list.union(account_list.filter(account_key=key))
            if 'DEBTOR:'+str(key) in data.keys() and data.get('DEBTOR:'+str(key)) == 'debtor':
                debtor_list = debtor_list.union(account_list.filter(account_key=key))
        if not debtor_list.first(): # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        if not creditor_list.first(): # Check for no creditors selected
            raise Http404('You must have creditors in your transaction.') # Complain
        context = super().get_context_data(**kwargs)
        context['creditor_list'] = creditor_list.order_by('type')
        context['debtor_list'] = debtor_list.order_by('type')
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

def CreateTransactionGroupAction(request):
    if request.method == 'POST':
        transaction_group = TransactionGroup()
        transaction_group.created_by = request.user
        transaction_group.save()
        data = request.POST
        account_list = Account.objects.all()
        creditor_list = Account.objects.none()
        debtor_list = Account.objects.none()
        for account in account_list:
            key = account.account_key
            if 'CREDITOR:'+str(key) in data.keys() and data.get('CREDITOR:'+str(key)) == 'creditor':
                creditor_list = creditor_list.union(account_list.filter(account_key=key))
            if 'DEBTOR:'+str(key) in data.keys() and data.get('DEBTOR:'+str(key)) == 'debtor':
                debtor_list = debtor_list.union(account_list.filter(account_key=key))
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        notes = data.get('notes')
        for creditor in creditor_list.all():
            transaction = Transaction()
            transaction.created_by = request.user
            transaction.transaction_group = transaction_group
            transaction.save()
            for debtor in debtor_list.all():
                key = 'AMOUNT:'+str(debtor.account_key)+':'+str(creditor.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry.create(account_a=creditor, account_b=debtor, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
    return redirect('UserPortalDashboard')

class DeleteTransaction(DeleteView):
    # Allows the treasurer to delete transactions
    pass
