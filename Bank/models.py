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
    open = models.BooleanField(default=True) # Is the account currently open? Use to keep list of current members to active members only.

    def __str__(self):
        if self.name:
            return '('+self.type+') '+self.name
        elif self.owner is not None:
            return '('+self.type+') '+self.owner.name()
        else:
            return '('+self.type+') **Nameless Account**'

class TransactionGroup(models.Model):
    # Holds multiple groups of Transaction objects, allowing single objects containing an entire set off accounts
    group_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?

    def set_date(self, date):
        # Sets the date for every transaction
        for transaction in self.transacton_set:
            transaction.set_date(date)

    def set_notes(self, notes):
        # Sets the notes on every transaction
        for transaction in self.transacton_set:
            transaction.set_notes(notes)

    def set_approved(self, approved):
        # Sets the approved status on every transaction
        for transaction in self.transacton_set:
            transaction.set_approved(approved)

    def __str__(self):
        return 'Transaction Group '+str(self.pk)

class Transaction(models.Model):
    # Parents the Entry model, allowing Many-To-One Transactions across multiple accounts
    transaction_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?
    transaction_group = models.ForeignKey(TransactionGroup, blank=True, null=True, on_delete=models.PROTECT)

    def set_date(self, date):
        # Sets the date for every entry
        for entry in self.entry_set.all():
            entry.date = date

    def set_notes(self, notes):
        # Sets the notes on every entry
        for entry in self.entry_set.all():
            entry.notes = notes

    def set_approved(self, approved):
        # Sets the approved status on every entry
        for entry in self.entry_set.all():
            entry.is_approved = approved

    def CreateEntry(self, account_a, account_b, credit_a, date, notes):
        # Calls the entry create entry method then adds it to the entry_set
        entry = Entry.create(account_a=account_a, account_b=account_b, credit_a=credit_a, date=date, notes=notes) # Create it
        entry.save() # Save it
        transacton.entry_set.add(entry) # Add it
        # Bop it

    @classmethod
    def create(cls, creditor, debtor_dict, date, notes):
        # Takes a single creditor, and a dictionary of {debtor: amount} items \
        # and produces an entry for each debtor, crediting the creditor and \
        # of each by the relevant amounts
        transaction = cls() # Create an empty transaction object
        for debtor, amount in debtor_dict:
            transacton.CreateEntry(account_a=creditor, account_b=debtor, credit_a=amount, date=date, notes=notes) # Create and add each entry to the object
        return transaction

    def __str__(self):
        return 'Transaction '+str(self.pk)

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
    is_approved = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.PROTECT)

    @classmethod
    def create(cls, account_a, account_b, credit_a, date, notes):
        entry = cls(account_a=account_a, account_b=account_b, credit_a=credit_a, date=date, notes=notes)
        return entry

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
        else:
            raise Exception("Cannot make transaction between account.type=='Pool' and account.type='Bank'")
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

class CustomCurrency(models.Model):
    # Allows custom "currencies," which are rates to be charged
    # CustomCurrencies can only be credited to users, and always debit a pool (negative credits for a charge)
    currency_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    credit = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # "Rate" of currency; the amount to credit an account by per unit
    pool = models.ForeignKey(Account, blank=False, null=False, on_delete=models.PROTECT) # The pool to be debited when someone is credited with this currency

    def save(self, *args, **kwargs):
        if self.pool is not None and self.pool.type != 'Pool':
          raise Exception("You must select a Pool account")
        super().save(*args, **kwargs)

class EventFeeTemplate(models.Model):
    # A set of currencies to provide the flesh of an Event model
    template_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    CustomCurrencies = models.ManyToManyField(CustomCurrency, blank=True, null=True) # Custom currencies that can be credited to users
    pools = models.ManyToManyField(Account, blank=True, null=True) # Pools that can be directly debited

    def save(self, *args, **kwargs):
        if self.pools is not None:
            for pool in self.pools.all():
                if pool.type != 'Pool':
                    raise Exception("You must select only Pool accounts")
        super().save(*args, **kwargs)

class Event(models.Model):
    # A wrapper for the TransactionGroup that integrates custom currecies \
    # to make doing the accounts for an event (a meet, a dinner, etc.) easier
    event_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    users = models.ManyToManyField(Account, blank=True, null=True) # User Accounts that can be credited
    transaction_group = models.OneToOneField(TransactionGroup, blank=False, null=False, on_delete=models.PROTECT, related_name='event') # The transaction group tied to the event
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?

    def save(self, *args, **kwargs):
        if self.users is not None:
            for user in self.users.all():
                if user.type != 'Pool':
                    raise Exception("You must select only User accounts")
        super().save(*args, **kwargs)
