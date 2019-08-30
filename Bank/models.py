from UserPortal.models import CustomUser
from django.db import models
from datetime import datetime
import uuid

ACCOUNT_TYPES = (
    ('Bank', 'Bank'),
    ('User', 'User'),
    ('Pool', 'Pool')
)

class Account(models.Model):
    # Representitive of legal entities. This could be the actual club account, a retailer that the club purchases from, or a member of the club
    account_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.OneToOneField(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='bank_account', help_text='If account is to be owned by a person, please select that user here.')
    name = models.CharField(max_length=100, blank=True, help_text='If account is unowned, please give it a sensible name.')
    type = models.CharField(max_length=100, blank=False, choices=ACCOUNT_TYPES)
    sort_name = models.CharField(max_length=100, blank=False, editable=False, default='-')

    def __str__(self):
        if self.name:
            return '('+self.type+') '+self.name
        elif self.owner is not None:
            return '('+self.type+') '+self.owner.name()
        else:
            return '('+self.type+') **Nameless Account**'

    def save(self, *args, **kwargs):
        self.sort_name = str(self)
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("view_own__account", "Can view own account"),
            ("view_other__account", "Can view others' accounts"),
        ]
        ordering = ['sort_name']

class CustomCurrency(models.Model):
    # Allows custom "currencies," which are rates to be charged
    # CustomCurrencies can only be credited to users, and always debit a pool (negative credits for a charge)
    currency_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    credit = models.DecimalField(max_digits=7, decimal_places=2, blank=False, help_text='The value of this currency in GBP. For a currency that will be a debit (charge), enter a negative number. For a currency that will be a credit, enter a positive number.') # "Rate" of currency; the amount to credit an account by per unit
    pool = models.ForeignKey(Account, blank=False, null=False, on_delete=models.PROTECT) # The pool to be debited when someone is credited with this currency
    def __str__(self):
        return self.name

class TransactionGroup(models.Model):
    # Holds multiple groups of Transaction objects, allowing single objects containing an entire set off accounts
    group_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT, related_name='created_transaction_group_set') # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?
    is_approved = models.BooleanField(default=False, editable=False)
    is_editable = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(CustomUser, blank=True, null=True, editable=False, on_delete = models.PROTECT, related_name='approved_transaction_group_set') # Who approved the object
    approved_on = models.DateTimeField(blank=True, null=True, default=datetime.now, editable=False) # When was the object approved?
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    notes = models.TextField(blank=True)

    def SetApprove(self, by=None, on=None, status=True):
        if status:
            self.is_approved = True
            self.approved_by = by
            self.approved_on = on
        else:
            self.is_approved = False
            self.approved_by = None
            self.approved_on = None
        for transaction in self.transaction_set.all():
            transaction.SetApprove(by, on, status)
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on)

    def depopulate(self):
        # deletes transactions owned by the transaction group
        for transaction in self.transaction_set.all():
            transaction.delete()

    def delete(self, orphan=False, *args, **kwargs):
        # by default, deleting a transaction group deletes its children and grandchildren
        if not orphan:
            self.depopulate()
        super().delete(*args, **kwargs)

    def __str__(self):
        return 'Transaction Group '+str(self.pk)

    class Meta:
        permissions = [
            ("approve__transactiongroup", "Can approve transaction groups"),
        ]

class Transaction(models.Model):
    # Parents the Entry model, allowing Many-To-One Transactions across multiple accounts
    transaction_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?
    transaction_group = models.ForeignKey(TransactionGroup, blank=True, null=True, on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=False, editable=False)
    is_editable = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(CustomUser, blank=True, null=True, editable=False, on_delete = models.PROTECT, related_name='approved_transaction_set') # Who approved the object
    approved_on = models.DateTimeField(blank=True, null=True, default=datetime.now, editable=False) # When was the object approved?
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    notes = models.TextField(blank=True)

    def SetApprove(self, by=None, on=None, status=True):
        if status:
            self.is_approved = True
            self.approved_by = by
            self.approved_on = on
        else:
            self.is_approved = False
            self.approved_by = None
            self.approved_on = None
        for entry in self.entry_set.all():
            entry.SetApprove(by, on, status)
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on)

    def depopulate(self):
        # deletes entries owned by the transaction group
        for entry in self.entry_set.all():
            entry.delete()

    def delete(self, orphan=False, *args, **kwargs):
        # by default, deleting a transaction deletes its children
        if not orphan:
            self.depopulate()
        super().delete(*args, **kwargs)

    def __str__(self):
        return 'Transaction '+str(self.pk)

    class Meta:
        permissions = [
            ("approve__transaction", "Can approve transactions"),
        ]

class Entry(models.Model):
    # The smallest unit of the transation family. Records an individual double-entry transaction
    entry_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?
    account_a = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT, related_name='transaction_set_a')
    account_b = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT, related_name='transaction_set_b')
    credit_a = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # Amount that account a has been credited by
    credit_b = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # Amount that account b has been credited by
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    notes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False, editable=False)
    transaction = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.PROTECT)
    is_editable = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(CustomUser, blank=True, null=True, editable=False, on_delete = models.PROTECT, related_name='approved_entry_set') # Who approved the object
    approved_on = models.DateTimeField(blank=True, null=True, default=datetime.now, editable=False) # When was the object approved?
    custom_currency = models.ForeignKey(CustomCurrency, on_delete=models.PROTECT, blank=True, null=True, editable=False)

    def SetApprove(self, by=None, on=None, status=True):
        if status:
            self.is_approved = True
            self.approved_by = by
            self.approved_on = on
        else:
            self.is_approved = False
            self.approved_by = None
            self.approved_on = None
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on)

    def save(self, *args, **kwargs):
        self.date = datetime(self.date.year, self.date.month, self.date.day, 12, 0, 0)
        if self.account_a.type == 'Bank' and self.account_b.type == 'Bank':
            self.credit_a = self.credit_a # Credit Account A
            self.credit_b = -self.credit_a # Debit To Account B
        elif self.account_a.type == 'Bank' and self.account_b.type == 'User':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = self.credit_a # Credit To Account
        elif self.account_a.type == 'User' and self.account_b.type == 'Bank':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = self.credit_a # Credit To Account
        elif self.account_a.type == 'User' and self.account_b.type == 'User':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = -self.credit_a # Debit To Account
        elif self.account_a.type == 'User' and self.account_b.type == 'Pool':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = -self.credit_a # Debit To Account
        elif self.account_a.type == 'Pool' and self.account_b.type == 'User':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = -self.credit_a # Debit To Account
        elif self.account_a.type == 'Pool' and self.account_b.type == 'Pool':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = -self.credit_a # Debit To Account
        elif self.account_a.type == 'Pool' and self.account_b.type == 'Bank':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = self.credit_a # Credit To Account
        elif self.account_a.type == 'Bank' and self.account_b.type == 'Pool':
            self.credit_a = self.credit_a # Credit From Account
            self.credit_b = self.credit_a # Credit To Account
        super().save(*args, **kwargs)

    def __str__(self):
        if self.credit_a >= 0 and self.credit_b >= 0:
            return '['+str(self.account_a)+' +'+str(self.credit_a)+']['+str(self.account_b)+' +'+str(self.credit_b)+']'
        if self.credit_a >= 0 and self.credit_b < 0:
            return '['+str(self.account_a)+' +'+str(self.credit_a)+']['+str(self.account_b)+' '+str(self.credit_b)+']'
        if self.credit_a < 0 and self.credit_b >= 0:
            return '['+str(self.account_a)+' '+str(self.credit_a)+']['+str(self.account_b)+' +'+str(self.credit_b)+']'
        if self.credit_a < 0 and self.credit_b < 0:
            return '['+str(self.account_a)+' '+str(self.credit_a)+']['+str(self.account_b)+' '+str(self.credit_b)+']'

    def short_id(self):
        return 'Entry '+str(self.pk)

    class Meta:
        permissions = [
            ("approve__entry", "Can approve entries"),
        ]

class FeeTemplate(models.Model):
    # A set of currencies to provide the flesh of an Event model
    template_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    custom_currency = models.ManyToManyField(CustomCurrency, blank=True) # Custom currencies that can be credited to users
    pools = models.ManyToManyField(Account, blank=True, related_name='fee_template_pool_set') # Pools that can be directly debited
    banks = models.ManyToManyField(Account, blank=True, related_name='fee_template_bank_set') # Bank accounts that can be directly debited

    def __str__(self):
        return self.name

class Event(models.Model):
    # A wrapper for the TransactionGroup that integrates custom currecies \
    # to make doing the accounts for an event (a meet, a dinner, etc.) easier
    event_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fee_template = models.ForeignKey(FeeTemplate, blank=False, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=False)
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    notes = models.TextField(blank=True)
    users = models.ManyToManyField(Account, blank=True) # User Accounts that can be credited
    transaction_group = models.OneToOneField(TransactionGroup, blank=False, null=True, on_delete=models.PROTECT, related_name='event') # The transaction group tied to the event
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?
    is_approved = models.BooleanField(default=False, editable=False)
    is_editable = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(CustomUser, blank=True, null=True, editable=False, on_delete = models.PROTECT, related_name='approved_event_set') # Who approved the object
    approved_on = models.DateTimeField(blank=True, null=True, default=datetime.now, editable=False) # When was the object approved?

    def SetApprove(self, by=None, on=None, status=True):
        if status:
            self.is_approved = True
            self.approved_by = by
            self.approved_on = on
        else:
            self.is_approved = False
            self.approved_by = None
            self.approved_on = None
        self.transaction_group.SetApprove(by, on, status)
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on)

    def delete(self, orphan=False, *args, **kwargs):
        # by default, deleting an event deletes its child, grand-children and great-grand-children
        if not orphan:
            transaction_group = self.transaction_group
            self.transaction_group = None
            self.save()
            transaction_group.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("approve__event", "Can approve events"),
        ]
