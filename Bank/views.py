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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

def BalanceAtDate(account, date=timezone.now(), all=False):
    # Returns the balance of an account at a date as a float
    if all: # allows retrieving of balance accounting for trasnactions that are in the future
        balance_a = account.transaction_set_a.all().aggregate(Sum('credit_a')).get('credit_a__sum')
        balance_b = account.transaction_set_b.all().aggregate(Sum('credit_b')).get('credit_b__sum')
    else:
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

@method_decorator(permission_required('Bank.add__entry'), name='dispatch')
class CreateEntry(FormView):
    form_class = CreateEntry
    template_name = 'Bank/AddEntry.html'
    def form_valid(self, form):
        from_account = form.cleaned_data['creditor']
        to_account = form.cleaned_data['debtor']
        amount = form.cleaned_data['amount']
        date = form.cleaned_data['date']
        notes = form.cleaned_data['notes']
        entry = Entry(account_a=from_account, account_b=to_account, credit_a=amount, date=date, notes=notes)
        entry.created_by = self.request.user
        entry.is_editable = True # set the editable bool on highest level
        entry.save()
        return super().form_valid(form)
    def get_success_url(self, **kwargs):
        return reverse_lazy('UserPortalDashboard')

@method_decorator(permission_required('Bank.change__entry'), name='dispatch')
class EditEntry(UpdateView):
    model = Entry
    template_name = 'Bank/EditEntry.html'
    slug_field = 'entry_key'
    fields = ['account_a', 'account_b', 'credit_a', 'date', 'notes']
    def get_success_url(self, **kwargs):
        # unset approved status
        self.object.SetApprove(status=False)
        return reverse_lazy('ViewEntry', args=(self.object.entry_key,))

@permission_required('Bank.approve__entry')
def ToggleApproveEntry(request, slug):
    # retrieve entry object
    entry = get_object_or_404(Entry, entry_key=slug, is_editable=True)
    # toggle the bool
    entry.ToggleApprove(request.user, datetime.now())
    return redirect('ViewEntry', entry.entry_key)

@permission_required('Bank.approve__transaction')
def ToggleApproveTransaction(request, slug):
    # retrieve the transaction object
    transaction = get_object_or_404(Transaction, transaction_key=slug, is_editable=True)
    # toggle the bool (automatically recurs through children)
    transaction.ToggleApprove(request.user, datetime.now())
    return redirect('ViewTransaction', transaction.transaction_key)

@permission_required('Bank.approve__transactiongroup')
def ToggleApproveTransactionGroup(request, slug):
    # retrieve the transaction group object
    transaction_group = get_object_or_404(TransactionGroup, group_key=slug, is_editable=True)
    # toggle the bool (automatically recurs through children)
    transaction_group.ToggleApprove(request.user, datetime.now())
    return redirect('ViewTransactionGroup', transaction_group.group_key)

@permission_required('Bank.approve__event')
def ToggleApproveEvent(request, slug):
    # retrieve the event object
    event = get_object_or_404(Event, event_key=slug, is_editable=True)
    # toggle the bool (automatically recurs through children)
    event.ToggleApprove(request.user, datetime.now())
    event.save()
    # recur into its transaction group, its transaction set, and their entry sets
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

@method_decorator(permission_required('Bank.view__customcurrency'), name='dispatch')
class ListCustomCurrency(ListView):
    model = CustomCurrency
    template_name = 'Bank/ListCustomCurrency.html'
    context_object_name = 'currency_list'

@method_decorator(permission_required('Bank.add__customcurrency'), name='dispatch')
class CreateCustomCurrency(CreateView):
    model = CustomCurrency
    form_class = CustomCurrencyForm
    template_name = 'Bank/AddCustomCurrency.html'
    success_url = reverse_lazy('ListCustomCurrency')

@method_decorator(permission_required('Bank.change__customcurrency'), name='dispatch')
class EditCustomCurrency(UpdateView):
    model = CustomCurrency
    form_class = CustomCurrencyForm
    slug_field = 'currency_key'
    template_name = 'Bank/EditCustomCurrency.html'
    success_url = reverse_lazy('ListCustomCurrency')

@method_decorator(permission_required('Bank.delete_customcurrency'), name='dispatch')
class DeleteCustomCurrency(DeleteView):
    model = CustomCurrency
    slug_field = 'currency_key'
    template_name = 'Bank/DeleteObject.html'
    success_url = reverse_lazy('ListCustomCurrency')

@method_decorator(permission_required('Bank.view__feetemplate'), name='dispatch')
class ListFeeTemplate(ListView):
    model = FeeTemplate
    template_name = 'Bank/ListFeeTemplate.html'
    context_object_name = 'template_list'

@method_decorator(permission_required('Bank.add__feetemplate'), name='dispatch')
class CreateFeeTemplate(CreateView):
    model = FeeTemplate
    form_class = FeeTemplateForm
    template_name = 'Bank/AddFeeTemplate.html'
    success_url = reverse_lazy('ListFeeTemplate')

@method_decorator(permission_required('Bank.change__feetemplate'), name='dispatch')
class EditFeeTemplate(UpdateView):
    model = FeeTemplate
    form_class = FeeTemplateForm
    slug_field = 'template_key'
    template_name = 'Bank/EditFeeTemplate.html'
    success_url = reverse_lazy('ListFeeTemplate')

@method_decorator(permission_required('Bank.delete__feetemplate'), name='dispatch')
class DeleteFeeTemplate(DeleteView):
    model = FeeTemplate
    slug_field = 'template_key'
    template_name = 'Bank/DeleteObject.html'
    success_url = reverse_lazy('ListFeeTemplate')

@method_decorator(permission_required('Bank.add__event'), name='dispatch')
class CreateEventSetup(TemplateView):
    template_name = 'Bank/AddEvent/Setup.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_list'] = FeeTemplate.objects.all().order_by('name')
        context['user_list'] = Account.objects.filter(type='User').order_by('type')
        context['date'] = datetime.now()
        return context

@method_decorator(permission_required('Bank.add__event'), name='dispatch')
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
        account_list = Account.objects.all().order_by('type')
        user_list = []
        for account in account_list:
            key = account.account_key
            if 'USER:'+str(key) in data.keys() and data.get('USER:'+str(key)) == 'user':
                user_list.append(account)
        if not user_list: # Check for no users selected
            raise Http404('You must have user in your event.') # Complain
        ## DATA PROCESSING
        # pass extracted data back to view
        context = super().get_context_data(**kwargs)
        context['name'] = name
        context['template'] = template
        context['user_list'] = user_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@permission_required('Bank.add__event')
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
        account_list = Account.objects.all().order_by('type')
        user_list = []
        for account in account_list:
            key = account.account_key
            if 'USER:'+str(key) in data.keys() and data.get('USER:'+str(key)) == 'user':
                user_list.append(account)
        ## DATA PROCESSING
        # create a transction group object
        transaction_group = TransactionGroup()
        transaction_group.created_by = request.user
        transaction_group.date = date
        transaction_group.notes = notes
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
            transaction.date = date
            transaction.notes = notes
            transaction.save()
            # entries for custom currencies
            for currency in template.custom_currency.all():
                key = 'AMOUNT:'+str(currency.currency_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and int(data.get(key)) != 0:
                    entry = Entry(account_a=user, account_b=currency.pool, credit_a=int(data.get(key))*float(currency.credit), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.custom_currency = currency # allows us to retrieve the event data
                    entry.save()
            # entries for pools
            for pool in template.pools.all():
                key = 'AMOUNT:'+str(pool.account_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry(account_a=user, account_b=pool, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
            # entries for banks
            for bank in template.banks.all():
                key = 'AMOUNT:'+str(bank.account_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry(account_a=user, account_b=bank, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
    return redirect('UserPortalDashboard')

@method_decorator(permission_required('Bank.view__event'), name='dispatch')
class ViewEvent(DetailView):
    model = Event
    template_name = 'Bank/ViewEvent.html'
    slug_field = 'event_key'

@method_decorator(permission_required('Bank.change__event'), name='dispatch')
class EditEventSetup(DetailView):
    model = Event
    slug_field = 'event_key'
    template_name = 'Bank/EditEvent/Setup.html'
    context_object_name = 'event'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template_list'] = FeeTemplate.objects.all().order_by('name')
        context['user_list'] = Account.objects.filter(type='User').order_by('type')
        return context

@method_decorator(permission_required('Bank.change__event'), name='dispatch')
class EditEventData(DetailView):
    model = Event
    slug_field = 'event_key'
    template_name = 'Bank/EditEvent/InputData.html'
    context_object_name = 'event'
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction group object
        self.object = self.get_object()
        # retrieve all post data (as dictionary of strings)
        data = request.POST
        # extract name
        name = data.get('name')
        # extract date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract fee template
        template = get_object_or_404(FeeTemplate, template_key=data.get('fee_template'))
        # extract user list
        account_list = Account.objects.all().order_by('type')
        user_list = []
        for account in account_list:
            key = account.account_key
            if 'USER:'+str(key) in data.keys() and data.get('USER:'+str(key)) == 'user':
                user_list.append(account)
        if not user_list: # Check for no users selected
            raise Http404('You must have user in your event.') # Complain
        ## DATA PROCESSING
        # pass extracted data back to view
        context = super().get_context_data(**kwargs)
        context['name'] = name
        context['template'] = template
        context['user_list'] = user_list.order_by('owner')
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction group object
        self.object = self.get_object()
        event = self.object
        # extract name
        name = event.name
        # extract date
        date = event.date
        # extract fee template
        template = event.fee_template
        # extract user list
        user_list = event.users.all()
        ## DATA PROCESSING
        # pass extracted data back to view
        context = super().get_context_data(**kwargs)
        context['name'] = name
        context['template'] = template
        context['user_list'] = user_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@permission_required('Bank.change__event')
def EditEventAction(request):
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
        user_list = []
        for account in account_list:
            key = account.account_key
            if 'USER:'+str(key) in data.keys() and data.get('USER:'+str(key)) == 'user':
                user_list.append(account)
        # retrieve event object
        event = get_object_or_404(Event, event_key=data.get('event'))
        transaction_group = event.transaction_group
        ## DATA PROCESSING
        # depopulate the transaction group
        transaction_group.depopulate()
        transaction_group.date = date
        transaction_group.notes = notes
        transaction_group.save()
        # create an event object, attach the transaction group
        event.fee_template = template
        event.name = name
        event.date = date
        event.notes = notes
        event.SetApprove(status=False)
        # clear and re-add users to event
        event.users.clear()
        for user in user_list.all():
            event.users.add(user)
        event.save()
        # create entries and transactions, and tie them to the event
        for user in user_list.all():
            # create transaction
            transaction = Transaction()
            transaction.created_by = request.user
            transaction.transaction_group = transaction_group
            transaction.date = date
            transaction.notes = notes
            transaction.save()
            # entries for custom currencies
            for currency in template.custom_currency.all():
                key = 'AMOUNT:'+str(currency.currency_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and int(data.get(key)) != 0:
                    entry = Entry(account_a=user, account_b=currency.pool, credit_a=int(data.get(key))*float(currency.credit), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.custom_currency = currency # allows us to retrieve the event data
                    entry.save()
            # entries for pools
            for pool in template.pools.all():
                key = 'AMOUNT:'+str(pool.account_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry(account_a=user, account_b=pool, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
            # entries for banks
            for bank in template.banks.all():
                key = 'AMOUNT:'+str(bank.account_key)+':'+str(user.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry(account_a=user, account_b=bank, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
    return redirect('ViewEvent', event.event_key)

@method_decorator(permission_required('Bank.delete__event'), name='dispatch')
class DeleteEvent(DeleteView):
    model = Event
    slug_field = 'event_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'

@method_decorator(permission_required('Bank.delete__entry'), name='dispatch')
class DeleteEntry(DeleteView):
    model = Entry
    slug_field = 'entry_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'

@method_decorator(permission_required('Bank.delete__transaction'), name='dispatch')
class DeleteTransaction(DeleteView):
    model = Transaction
    slug_field = 'transaction_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'

@method_decorator(permission_required('Bank.delete__transactiongroup'), name='dispatch')
class DeleteTransactionGroup(DeleteView):
    model = TransactionGroup
    slug_field = 'group_key'
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'Bank/DeleteObject.html'

@method_decorator(permission_required('Bank.add__account'), name='dispatch')
class CreateAccount(CreateView):
    model = Account
    template_name = 'Bank/AddAccount.html'
    fields = '__all__'
    success_url = reverse_lazy('UserPortalDashboard')

@method_decorator(permission_required('Bank.change__account'), name='dispatch')
class EditAccount(UpdateView):
    model = Account
    template_name = 'Bank/EditAccount.html'
    slug_field = 'account_key'
    fields = '__all__'
    success_url = reverse_lazy('UserPortalDashboard')

@method_decorator(permission_required('Bank.delete__account'), name='dispatch')
class DeleteAccount(DeleteView):
    model = Account
    template_name = 'Bank/DeleteObject.html'
    slug_field = 'account_key'
    fields = '__all__'
    success_url = reverse_lazy('UserPortalDashboard')

@method_decorator(permission_required('Bank.view_own__account'), name='dispatch')
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
        # handling for date filters
        if self.request.method == 'GET':
            # check if start date has been set
            if 'start_date' in self.request.GET and self.request.GET['start_date']:
                # extract start date and create datetime object with it
                start_date = datetime.strptime(self.request.GET['start_date'], '%Y-%m-%d')
                context['view_earliest'] = False
            else:
                # check that there are some entries
                if entry_set.exists():
                    # set start date to date and time of earliest entry in list
                    start_date = entry_set.order_by('date')[0].date
                else:
                    # if no entries, start date and time is now
                    start_date = datetime.now()
                context['view_earliest'] = True
            # set start date time to 00:00 to ensure dates are inclusive
            start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            context['start_date'] = start_date
            # check if end date has been set
            if 'end_date' in self.request.GET and self.request.GET['end_date']:
                # extract end date and create datetime object with it
                end_date = datetime.strptime(self.request.GET['end_date'], '%Y-%m-%d')
                context['view_latest'] = False
            else:
                if entry_set.exists():
                    end_date = entry_set.order_by('-date')[0].date
                else:
                    end_date = datetime.now()
                context['view_latest'] = True
            # set end date time to 23:59 to ensure dates are inclusive
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            context['end_date'] = end_date
            # calculate balances at start and end dates
            context['start_balance'] = BalanceAtDate(account, start_date)
            context['end_balance'] = BalanceAtDate(account, end_date)
            # retrieve properly ordered and filtered entry set within start and end dates
            context['entry_set'] = account.transaction_set_a.filter(date__range=(start_date, end_date)).union(account.transaction_set_b.filter(date__range=(start_date, end_date))).order_by('-date')
        return context

@method_decorator(permission_required('Bank.view_other__account'), name='dispatch')
class ListAccounts(ListView):
    model = Account
    template_name = 'Bank/ListAccounts.html'
    context_object_name = 'account_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # recover account list
        accounts_list = context['account_list']
        # generate balance for each account
        balance_list = []
        for account in accounts_list:
            balance_list.append(BalanceAtDate(account, all=True))
        # combine account and balance lists into dict for easier parsing in template
        context['account_dict'] = dict(zip(accounts_list, balance_list))
        return context

@method_decorator(permission_required('Bank.view__transaction'), name='dispatch')
class ViewTransaction(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/ViewTransaction.html'

@method_decorator(permission_required('Bank.view__transactiongroup'), name='dispatch')
class ViewTransactionGroup(DetailView):
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/ViewTransactionGroup.html'

@method_decorator(permission_required('Bank.view__entry'), name='dispatch')
class ViewEntry(DetailView):
    model = Entry
    slug_field = 'entry_key'
    context_object_name = 'entry'
    template_name = 'Bank/ViewEntry.html'

@method_decorator(permission_required('Bank.add__transaction'), name='dispatch')
class CreateTransactionCreditor(TemplateView):
    # Allows the treasurer to create transactions
    template_name = 'Bank/AddTransaction/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

@method_decorator(permission_required('Bank.add__transaction'), name='dispatch')
class CreateTransactionDebtor(TemplateView):
    # Allows the treasurer to create transactions
    template_name = 'Bank/AddTransaction/SelectDebtor.html'
    def post(self, request, *args, **kwargs):
        data = request.POST
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        account_list = Account.objects.all().order_by('type')
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@method_decorator(permission_required('Bank.add__transaction'), name='dispatch')
class CreateTransactionData(TemplateView):
    template_name = 'Bank/AddTransaction/InputData.html'
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # extract POST data
        data = request.POST
        # extract date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract creditor
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        # extract list of debtors
        all_accounts = Account.objects.all().order_by('type')
        account_list = []
        for account in all_accounts:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'TRUE':
                account_list.append(account)
        if not account_list: # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        ## DATA PROCESSING
        # pass retrived data into next page of form
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@permission_required('Bank.add__transaction')
def CreateTransactionAction(request):
    if request.method == 'POST':
        ## DATA RETRIEVAL
        # extract POST data
        data = request.POST
        # extract creditor
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        # extract date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        # extract notes
        notes = data.get('notes')
        ## DATA PROCESSING
        # create a transaction object
        transaction = Transaction(is_editable=True)
        transaction.created_by = request.user
        transaction.date = date
        transaction.notes = notes
        transaction.save()
        # create entries for all debtors
        account_list = Account.objects.all()
        for account in account_list:
            key = str(account.account_key)
            if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                debtor = account
                amount = data.get(key)
                entry = Entry(account_a=creditor, account_b=debtor, credit_a=float(amount), date=date, notes=notes)
                entry.created_by = request.user
                entry.transaction = transaction
                entry.save()
    return redirect('ViewTransaction', transaction.transaction_key)

@method_decorator(permission_required('Bank.change__transaction'), name='dispatch')
class EditTransactionCreditor(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/EditTransaction/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pass data to template to pre-populate form
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

@method_decorator(permission_required('Bank.change__transaction'), name='dispatch')
class EditTransactionDebtor(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/EditTransaction/SelectDebtor.html'
    # POST for when we have come from "select creditor" view
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction object
        self.object = self.get_object()
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract the creditor
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        account_list = Account.objects.all().order_by('type')
        ## DATA PROCESSING
        # pass data to template to populate form
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)
    # GET for when we want to change debtors (and not creditors)
    def get(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction object
        self.object = self.get_object()
        # extract the date
        date = self.object.entry_set.first().date
        # extract the creditor
        creditor = self.object.entry_set.first().account_a
        account_list = Account.objects.all().order_by('type')
        ## DATA PROCESSING
        # pass the data to the template to populate form
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@method_decorator(permission_required('Bank.change__transaction'), name='dispatch')
class EditTransactionData(DetailView):
    model = Transaction
    slug_field = 'transaction_key'
    context_object_name = 'transaction'
    template_name = 'Bank/EditTransaction/InputData.html'
    # POST for when we have come from "select debtors" view
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction object
        self.object = self.get_object()
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract the creditor
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        # extract the debtor list
        all_accounts = Account.objects.all().order_by('type')
        account_list = []
        for account in all_accounts:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'TRUE':
                account_list.append(account)
        if not account_list: # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        ## DATA PROCESSING
        # pass the data to the template to populate the form
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)
    # GET for when we want to directly change the data but not the creditors or the debtors
    def get(self, request, *args, **kwargs):
        # get the transaction object
        self.object = self.get_object()
        # extract the date
        date = self.object.date
        # extract the creditor
        creditor = self.object.entry_set.first().account_a
        # extract the debtor list
        account_list = []
        for entry in self.object.entry_set.all():
            account_list.append(get_object_or_404(Account, account_key=entry.account_b.account_key))
        ## DATA PROCESSING
        # pass the data to the template to populate the form
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor'] = creditor
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@permission_required('Bank.change__transaction')
def EditTransactionAction(request):
    if request.method == 'POST':
        ## DATA RETRIEVAL
        # extract the POST data
        data = request.POST
        # extract the creditor
        creditor = get_object_or_404(Account, account_key=data.get('creditor'))
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        # extract the notes
        notes = data.get('notes')
        # get the transaction object
        transaction = get_object_or_404(Transaction, transaction_key=data.get('transaction'))
        ## DATA PROCESSING
        # delete all its entry children
        transaction.depopulate()
        transaction.notes = notes
        transaction.date = date
        transaction.save()
        # set approved status to false
        transaction.SetApprove(status=False)
        # recreate new entries from the data
        account_list = Account.objects.all()
        for account in account_list:
            key = str(account.account_key)
            if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                debtor = account
                amount = data.get(key)
                entry = Entry(account_a=creditor, account_b=debtor, credit_a=float(amount), date=date, notes=notes)
                entry.created_by = request.user
                entry.transaction = transaction
                entry.save()
    return redirect('ViewTransaction', transaction.transaction_key)

@method_decorator(permission_required('Bank.add__transactiongroup'), name='dispatch')
class CreateTransactionGroupCreditor(TemplateView):
    template_name = 'Bank/AddTransactionGroup/SelectCreditor.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_list'] = Account.objects.all().order_by('type')
        context['date'] = datetime.now()
        return context

@method_decorator(permission_required('Bank.add__transactiongroup'), name='dispatch')
class CreateTransactionGroupDebtor(TemplateView):
    template_name = 'Bank/AddTransactionGroup/SelectDebtor.html'
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract the list of creditors
        account_list = Account.objects.all().order_by('type')
        creditor_list = []
        for account in account_list:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'creditor':
                creditor_list.append(account)
        if not creditor_list: # Check for no debtors selected
            raise Http404('You must have creditors in your transaction.') # Complain
        # DATA PROCESSING
        # pass the data to the template
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor_list'] = creditor_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@method_decorator(permission_required('Bank.add__transactiongroup'), name='dispatch')
class CreateTransactionGroupData(TemplateView):
    template_name = 'Bank/AddTransactionGroup/InputData.html'
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract the lists of debtors and creditors
        account_list = Account.objects.all().order_by('type')
        creditor_list = []
        debtor_list = []
        for account in account_list:
            key = account.account_key
            if 'CREDITOR:'+str(key) in data.keys() and data.get('CREDITOR:'+str(key)) == 'creditor':
                creditor_list.append(account)
            if 'DEBTOR:'+str(key) in data.keys() and data.get('DEBTOR:'+str(key)) == 'debtor':
                debtor_list.append(account)
        if not debtor_list: # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        if not creditor_list: # Check for no creditors selected
            raise Http404('You must have creditors in your transaction.') # Complain
        ## DATA PROCESSING
        # pass the data to the template
        context = super().get_context_data(**kwargs)
        context['creditor_list'] = creditor_list
        context['debtor_list'] = debtor_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@permission_required('Bank.add__transactiongroup')
def CreateTransactionGroupAction(request):
    if request.method == 'POST':
        ## DATA RETRIEVAL
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        # extract the notes
        notes = data.get('notes')
        # extract the lists of creditors and debtors
        account_list = Account.objects.all()
        creditor_list = []
        debtor_list = []
        for account in account_list:
            key = account.account_key
            if 'CREDITOR:'+str(key) in data.keys() and data.get('CREDITOR:'+str(key)) == 'creditor':
                creditor_list.append(account)
            if 'DEBTOR:'+str(key) in data.keys() and data.get('DEBTOR:'+str(key)) == 'debtor':
                debtor_list.append(account)
        ## DATA PROCESSING
        # create a transaction group object
        transaction_group = TransactionGroup(is_editable=True)
        transaction_group.created_by = request.user
        transaction_group.date = date
        transaction_group.notes = notes
        transaction_group.save()
        # create transaction children and entry grand-children
        for creditor in creditor_list.all():
            transaction = Transaction()
            transaction.created_by = request.user
            transaction.transaction_group = transaction_group
            transaction.date = date
            transaction.notes = notes
            transaction.save()
            for debtor in debtor_list.all():
                key = 'AMOUNT:'+str(debtor.account_key)+':'+str(creditor.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry(account_a=creditor, account_b=debtor, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
    return redirect('ViewTransactionGroup', transaction_group.group_key)

@method_decorator(permission_required('Bank.change__transactiongroup'), name='dispatch')
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

@method_decorator(permission_required('Bank.change__transactiongroup'), name='dispatch')
class EditTransactionGroupDebtor(DetailView):
    # Allows the treasurer to create transactions
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/EditTransactionGroup/SelectDebtor.html'
    # POST for when we've come from the "edit creditors" page
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction group object
        self.object = self.get_object()
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract the list of creditors
        account_list = Account.objects.all().order_by('type')
        creditor_list = []
        for account in account_list:
            key = account.account_key
            if str(key) in data.keys() and data.get(str(key)) == 'creditor':
                creditor_list.append(account)
        if not creditor_list: # Check for no debtors selected
            raise Http404('You must have creditors in your transaction.') # Complain
        ## DATA PROCESSING
        # pass the data to the template
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor_list'] = creditor_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)
    # GET for when we skipped editing creditors
    def get(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get the transaction group object
        self.object = self.get_object()
        # extract the date
        date = self.object.transaction_set.first().entry_set.first().date
        # extract the list of creditors
        creditor_list = []
        account_list = Account.objects.all().order_by('type')
        for transaction in self.object.transaction_set.all():
            for entry in transaction.entry_set.all():
                creditor_list.append(get_object_or_404(Account, account_key=entry.account_a.account_key))
        # DATA PROCESSING
        # pass the data to the template
        context = super().get_context_data(**kwargs)
        context['account_list'] = account_list
        context['creditor_list'] = creditor_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@method_decorator(permission_required('Bank.change__transactiongroup'), name='dispatch')
class EditTransactionGroupData(DetailView):
    model = TransactionGroup
    slug_field = 'group_key'
    context_object_name = 'transaction_group'
    template_name = 'Bank/EditTransactionGroup/InputData.html'
    # POST for when we came from the "edit debtors" page
    def post(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get transction group object
        self.object = self.get_object()
        # extract the POST data
        data = request.POST
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        # extract the lists of creditors and debtors
        account_list = Account.objects.all().order_by('type')
        creditor_list = []
        debtor_list = []
        for account in account_list:
            key = account.account_key
            if 'CREDITOR:'+str(key) in data.keys() and data.get('CREDITOR:'+str(key)) == 'creditor':
                creditor_list.append(account)
            if 'DEBTOR:'+str(key) in data.keys() and data.get('DEBTOR:'+str(key)) == 'debtor':
                debtor_list.append(account)
        if not debtor_list: # Check for no debtors selected
            raise Http404('You must have debtors in your transaction.') # Complain
        if not creditor_list: # Check for no creditors selected
            raise Http404('You must have creditors in your transaction.') # Complain
        ## DATA PROCESSING
        # pass the data to the template
        context = super().get_context_data(**kwargs)
        context['creditor_list'] = creditor_list
        context['debtor_list'] = debtor_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)
    # GET for when we skipped editing debtors and creditors
    def get(self, request, *args, **kwargs):
        ## DATA RETRIEVAL
        # get transaction group object
        self.object = self.get_object()
        # extract the date
        date = self.object.transaction_set.first().entry_set.first().date
        # extract the lists of creditors and debtors
        creditor_list = []
        debtor_list =  []
        for transaction in self.object.transaction_set.all():
            for entry in transaction.entry_set.all():
                creditor_list.append(get_object_or_404(Account, account_key=entry.account_a.account_key))
                debtor_list.append(get_object_or_404(Account, account_key=entry.account_b.account_key))
        ## DATA PROCESSING
        # pass the data to the template
        context = super().get_context_data(**kwargs)
        context['creditor_list'] = creditor_list
        context['debtor_list'] = debtor_list
        context['date'] = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        return render(request, self.template_name, context)

@permission_required('Bank.change__transactiongroup')
def EditTransactionGroupAction(request):
    if request.method == 'POST':
        ## DATA RETRIEVAL
        # extract the POST data
        data = request.POST
        # retrieve the transaction group object
        transaction_group = get_object_or_404(TransactionGroup, group_key=data.get('transaction_group'))
        # extract the lists of creditors and debtors
        account_list = Account.objects.all()
        creditor_list = []
        debtor_list = []
        for account in account_list:
            key = account.account_key
            if 'CREDITOR:'+str(key) in data.keys() and data.get('CREDITOR:'+str(key)) == 'creditor':
                creditor_list.append(account)
            if 'DEBTOR:'+str(key) in data.keys() and data.get('DEBTOR:'+str(key)) == 'debtor':
                debtor_list.append(account)
        # extract the date
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        date = datetime(date.year, date.month, date.day, 12, 0, 0) # All transactions happen at Mid Day
        # extract the notes
        notes = data.get('notes')
        ## DATA PROCESSING
        # delete all children and grand-children
        transaction_group.depopulate()
        transaction_group.notes = notes
        transaction_group.date = date
        transaction_group.save()
        # unset the approved status
        transaction_group.SetApprove(status=False)
        # create new transaction children and entry grand-children from new data
        for creditor in creditor_list.all():
            transaction = Transaction()
            transaction.created_by = request.user
            transaction.transaction_group = transaction_group
            transaction.date = date
            transaction.notes = notes
            transaction.save()
            for debtor in debtor_list.all():
                key = 'AMOUNT:'+str(debtor.account_key)+':'+str(creditor.account_key)
                if key in data.keys() and data.get(key) and float(data.get(key)) != 0.0:
                    entry = Entry(account_a=creditor, account_b=debtor, credit_a=float(data.get(key)), date=date, notes=notes)
                    entry.created_by = request.user
                    entry.transaction = transaction
                    entry.save()
    return redirect('ViewTransactionGroup', transaction_group.group_key)
