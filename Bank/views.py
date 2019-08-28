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
from django.http import HttpResponseRedirect

def TransactionsToDate(account, date=timezone.now()):
    # Returns a query set of all transactions up to a date on an account
    return account.transaction_set.filter(date__lte=date)

def BalanceAtDate(account, date=timezone.now()):
    # Returns the balance of an account at a date as a float
    balance_a = account.transaction_set_a.filter(date__lte=date).aggregate(Sum('credit_a')).get('credit_a__sum')
    balance_b = account.transaction_set_b.filter(date__lte=date).aggregate(Sum('credit_b')).get('credit_b__sum')
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
        entry.is_editable = True # set the editable bool on highest level
        entry.save()
        return super().form_valid(form)

class EditEntry(UpdateView):
    model = Entry
    template_name = 'Bank/EditEntry.html'
    slug_field = 'entry_key'
    success_url = reverse_lazy('UserPortalDashboard')
    fields = ['account_a', 'account_b', 'credit_a', 'date', 'notes']

def ToggleApproveEntry(request, slug):
    entry = get_object_or_404(Entry, entry_key=slug, is_editable=True)
    entry.is_approved = not entry.is_approved
    if entry.is_approved:
        entry.approved_by = request.user
        entry.approved_on = datetime.now()
    entry.save()
    return redirect('ViewEntry', entry.entry_key)

def ToggleApproveTransaction(request, slug):
    transaction = get_object_or_404(Transaction, transaction_key=slug, is_editable=True)
    transaction.is_approved = not transaction.is_approved
    if transaction.is_approved:
        transaction.approved_by = request.user
        transaction.approved_on = datetime.now()
    transaction.save()
    for entry in transaction.entry_set.all():
            entry.is_approved = transaction.is_approved
            if entry.is_approved:
                entry.approved_by = request.user
                entry.approved_on = datetime.now()
            entry.save()
    return redirect('ViewTransaction', transaction.transaction_key)

def ToggleApproveTransactionGroup(request, slug):
    transaction_group = get_object_or_404(TransactionGroup, group_key=slug, is_editable=True)
    transaction_group.is_approved = not transaction_group.is_approved
    if transaction_group.is_approved:
        transaction_group.approved_by = request.user
        transaction_group.approved_on = datetime.now()
    transaction_group.save()
    for transaction in transaction_group.transaction_set.all():
        transaction.is_approved = transaction_group.is_approved
        if transaction.is_approved:
            transaction.approved_by = request.user
            transaction.approved_on = datetime.now()
        transaction.save()
        for entry in transaction.entry_set.all():
                entry.is_approved = transaction_group.is_approved
                if entry.is_approved:
                    entry.approved_by = request.user
                    entry.approved_on = datetime.now()
                entry.save()
    return redirect('ViewTransactionGroup', transaction_group.group_key)

def ToggleApproveEvent(request, slug):
    event = get_object_or_404(Event, event_key=slug, is_editable=True)
    event.is_approved = not event.is_approved
    if event.is_approved:
        event.approved_by = request.user
        event.approved_on = datetime.now()
    event.save()
    transaction_group = event.transaction_group
    transaction_group.is_approved = event.is_approved
    for transaction in transaction_group.transaction_set.all():
        transaction.is_approved = transaction_group.is_approved
        if transaction_group.is_approved:
            transaction_group.approved_by = request.user
            transaction_group.approved_on = datetime.now()
        transaction_group.save()
        if transaction.is_approved:
            transaction.approved_by = request.user
            transaction.approved_on = datetime.now()
        transaction.save()
        for entry in transaction.entry_set.all():
                entry.is_approved = transaction_group.is_approved
                if entry.is_approved:
                    entry.approved_by = request.user
                    entry.approved_on = datetime.now()
                entry.save()
    return redirect('ViewEvent', event.event_key)


class ListCustomCurrency(ListView):
    model = CustomCurrency
    template_name = 'Bank/ListCustomCurrency.html'
    context_object_name = 'currency_list'

class CreateCustomCurrency(CreateView):
    model = CustomCurrency
    form_class = CustomCurrencyForm
    template_name = 'Bank/AddCustomCurrency.html'
    success_url = reverse_lazy('ListCustomCurrency')

class EditCustomCurrency(UpdateView):
    model = CustomCurrency
    form_class = CustomCurrencyForm
    slug_field = 'currency_key'
    template_name = 'Bank/EditCustomCurrency.html'
    success_url = reverse_lazy('ListCustomCurrency')

class DeleteCustomCurrency(DeleteView):
    model = CustomCurrency
    slug_field = 'currency_key'
    template_name = 'Bank/DeleteObject.html'
    success_url = reverse_lazy('ListCustomCurrency')


class ListFeeTemplate(ListView):
    model = FeeTemplate
    template_name = 'Bank/ListFeeTemplate.html'
    context_object_name = 'template_list'

class CreateFeeTemplate(CreateView):
    model = FeeTemplate
    form_class = FeeTemplateForm
    template_name = 'Bank/AddFeeTemplate.html'
    success_url = reverse_lazy('ListFeeTemplate')

class EditFeeTemplate(UpdateView):
    model = FeeTemplate
    form_class = FeeTemplateForm
    slug_field = 'template_key'
    template_name = 'Bank/EditFeeTemplate.html'
    success_url = reverse_lazy('ListFeeTemplate')

class DeleteFeeTemplate(DeleteView):
    model = FeeTemplate
    slug_field = 'template_key'
    template_name = 'Bank/DeleteObject.html'
    success_url = reverse_lazy('ListFeeTemplate')


class CreateEventSetup(TemplateView):
    template_name = 'Bank/AddEvent/Setup.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_list'] = FeeTemplate.objects.all().order_by('name')
        context['user_list'] = Account.objects.filter(type='User').order_by('type')
        context['date'] = datetime.now()
        return context

class CreateEventData(TemplateView):
    template_name = 'Bank/AddEvent/InputData.html'
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # retrieve all post data (as dictionary of strings)
        data = request.POST
        # extract name
        name = data.get('name')
        # extract date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract fee template
        template = get_object_or_404(FeeTemplate, template_key=data.get('fee_template'))
        # extract user list
        account_list = Account.objects.all()
        user_list = Account.objects.none()
        for account in account_list:
            key = account.account_key
            if 'USER:'+str(key) in data.keys() and data.get('USER:'+str(key)) == 'user':
                user_list = user_list.union(account_list.filter(account_key=key))
        if not user_list.first(): # Check for no users selected
            raise Http404('You must have user in your event.') # Complain
        ## DATA PROCESSING
        # pass extracted data back to view
        context = super().get_context_data(**kwargs)
        context['name'] = name
        context['template'] = template
        context['user_list'] = user_list.order_by('owner')
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

def CreateEventAction(request):
    if request.method == 'POST':
        ## DATA RETRIEVAL
        # retrieve all POST data
        data = request.POST
        # extract name
        name = data.get('name')
        # extract date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        # extract notes
        notes = data.get('notes')
        # extract fee template
        template = get_object_or_404(FeeTemplate, template_key=data.get('fee_template'))
        # extract user list
        account_list = Account.objects.all()
        user_list = Account.objects.none()
        for account in account_list:
            key = account.account_key
            if 'USER:'+str(key) in data.keys() and data.get('USER:'+str(key)) == 'user':
                user_list = user_list.union(account_list.filter(account_key=key))
        ## DATA PROCESSING
        # create a transction group object
        transaction_group = TransactionGroup()
        transaction_group.created_by = request.user
        transaction_group.save()
        # create an event object, attach the transaction group
        event = Event()
        event.is_editable = True
        event.created_by = request.user
        event.created_on = datetime.now()
        event.transaction_group = transaction_group
        event.fee_template = template
        event.name = name
        event.date = date
        event.notes = notes
        event.save()
        # add users to event
        for user in user_list.all():
            event.users.add(user)
        # create entries and transactions, and tie them to the event
        for user in user_list.all():
            # create transaction
            transaction = Transaction()
            transaction.created_by = request.user
            transaction.transaction_group = transaction_group
            transaction.save()
            # entries for custom currencies
            for currency in template.custom_currency.all():
                key = 'AMOUNT:'+str(currency.currency_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and int(data.get(key)) != 0:
                    entry = Entry.create(account_a=user, account_b=currency.pool, credit_a=int(data.get(key))*float(currency.credit), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.custom_currency = currency # allows us to retrieve the event data
                    entry.save()
            # entries for pools
            for pool in template.pools.all():
                key = 'AMOUNT:'+str(pool.account_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry.create(account_a=user, account_b=pool, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
            # entries for banks
            for bank in template.banks.all():
                key = 'AMOUNT:'+str(bank.account_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry.create(account_a=user, account_b=bank, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
    return redirect('UserPortalDashboard')

class ViewEvent(DetailView):
    model = Event
    template_name = 'Bank/ViewEvent.html'
    slug_field = 'event_key'

class EditEventSetup(DetailView):
    pass

class EditEventData(DetailView):
    pass

def EditEventAction(request):
    pass

class DeleteEvent(DeleteView):
    pass

class DeleteEntry(DeleteView):
    model = Entry
    slug_field = 'entry_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'

class DeleteTransaction(DeleteView):
    model = Transaction
    slug_field = 'transaction_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        for entry in self.object.entry_set.all():
            entry.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class DeleteTransactionGroup(DeleteView):
    model = TransactionGroup
    slug_field = 'group_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        for transaction in self.object.transaction_set.all():
            for entry in transaction.entry_set.all():
                entry.delete()
            transaction.delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class CreateAccount(CreateView):
    model = Account
    template_name = 'Bank/AddAccount.html'
    fields = '__all__'
    success_url = reverse_lazy('UserPortalDashboard')

class EditAccount(UpdateView):
    model = Account
    template_name = 'Bank/EditAccount.html'
    slug_field = 'account_key'
    fields = '__all__'
    success_url = reverse_lazy('UserPortalDashboard')

class DeleteAccount(DeleteView):
    model = Account
    template_name = 'Bank/DeleteObject.html'
    slug_field = 'account_key'
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
                if entry_set.exists():
                    start_date = entry_set.order_by('date')[0].date
                else:
                    start_date = datetime.now()
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                print(start_date)
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
            context['entry_set'] = account.transaction_set_a.filter(date__range=(start_date, end_date)).union(account.transaction_set_b.filter(date__range=(start_date, end_date))).order_by('-date')
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
        transaction = Transaction(is_editable=True)
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
        transaction_group = TransactionGroup(is_editable=True)
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

class EditTransactionGroupCreditor(DetailView):
    # Allows the treasurer to create transactions
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/EditTransactionGroup/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

class EditTransactionGroupDebtor(DetailView):
    # Allows the treasurer to create transactions
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/EditTransactionGroup/SelectDebtor.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        date = self.object.transaction_set.first().entry_set.first().date
        creditor_list = Account.objects.none()
        account_list = Account.objects.all()
        for transaction in self.object.transaction_set.all():
            for entry in transaction.entry_set.all():
                creditor_list = creditor_list.union(Account.objects.filter(account_key=entry.account_a.account_key))
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list.order_by('type')
        context['creditor_list'] = creditor_list.order_by('type')
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

class EditTransactionGroupData(DetailView):
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/EditTransactionGroup/InputData.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        date = self.object.transaction_set.first().entry_set.first().date
        creditor_list = Account.objects.none()
        debtor_list = Account.objects.none()
        for transaction in self.object.transaction_set.all():
            for entry in transaction.entry_set.all():
                creditor_list = creditor_list.union(Account.objects.filter(account_key=entry.account_a.account_key))
                debtor_list = debtor_list.union(Account.objects.filter(account_key=entry.account_b.account_key))
        context = super().get_context_data(**kwargs)
        context['creditor_list'] = creditor_list.order_by('type')
        context['debtor_list'] = debtor_list.order_by('type')
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

def EditTransactionGroupAction(request):
    if request.method == 'POST':
        data = request.POST
        transaction_group = get_object_or_404(TransactionGroup, group_key=data.get('transaction_group'))
        for transaction in transaction_group.transaction_set.all(): # remove all previous entries
            for entry in transaction.entry_set.all():
                entry.delete()
            transaction.delete()
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
