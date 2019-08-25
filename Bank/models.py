from UserPortal.models import CustomUser
from django.db import models
from datetime import datetime
import uuid

ACCOUNT_TYPES = (
    ('Bank', 'Bank'),
    ('User', 'User'),
    ('Pool', 'Pool')
)

"""
Some Terminology:
Book:
    Representitive of pools or categories of money.
    Transactions that appear on a Book show the flow of credit and debt for that category.
    If a book shows a positve sum balance, then this is a source of income for the club.
    If a book shows a negative sum balance, then this is a source of outgoings for the club.
    Each transaction on a book shows:
    - Account: The account of the entity involved in the transaction
    - Credit/Debit: The amount that has been credited/debited. The book credit = the account debit (and vice-versa)
    - Date: When the transaction took place
    - Notes (Optional): Any useful notes about the transaction

Ledger:
    Representitive of a real bank account.
    Transactions on the ledger each correspond exactly to a transacion on the bank account.
    Each transaction on the ledger shows:
    - Account: The account of the entity involved in the transaction
    - Credit/Debit: The amount of money that went from one to the other
    - Date: When the transaction took place
    - Notes (Optional): Any useful notes about the transaction

Statement:
    Similar to a book, but refers to the record of transactions on an external entity's account
    Each transaction on a statement shows:
    - Type: Book, Bank, or Swap?
    - Account: The book, bank account, or entity account involved in the transacion
    - Credit/Debit: How much the entity has been credited/Debited by
"""

class Account(models.Model):
    # Representitive of legal entities. This could be the actual club account, a retailer that the club purchases from, or a member of the club
    account_key = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='bank_account', help_text='If account is to be owned by a person, please select that user here.')
    name = models.CharField(max_length=100, blank=True, help_text='If account is unowned, please give it a sensible name.')
    type = models.CharField(max_length=100, blank=False, choices=ACCOUNT_TYPES)

    def __str__(self):
        if self.name:
            return '('+self.type+') '+self.name
        elif self.owner is not None:
            return '('+self.type+') '+self.owner.name()
        else:
            return '('+self.type+') **Nameless Account**'

class Entry(models.Model):
    # The smallest unit of the transation family. Records an individual double-entry transaction
    entry_key = models.UUIDField(default=uuid.uuid4, editable=False)
    account_a = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT, related_name='transacton_set_a')
    account_b = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT, related_name='transaction_set_b')
    credit_a = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # Amount that account a has been credited by
    credit_b = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # Amount that account b has been credited by
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    notes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)

    @classmethod
    def create(cls, account_a, account_b, credit_a, date, notes):
        if account_a.type == 'Bank' and account_b.type == 'Bank':
            credit_a = credit_a # Credit Account A
            credit_b = -credit_a # Debit To Account B
        elif account_a.type == 'Bank' and account_b.type == 'User':
            credit_a = credit_a # Credit From Account
            credit_b = credit_a # Credit To Account
        elif account_a.type == 'User' and account_b.type == 'Bank':
            credit_a = credit_a # Credit From Account
            credit_b = credit_a # Credit To Account
        elif account_a.type == 'User' and account_b.type == 'User':
            credit_a = credit_a # Credit From Account
            credit_b = -credit_a # Debit To Account
        elif account_a.type == 'User' and account_b.type == 'Pool':
            credit_a = credit_a # Credit From Account
            credit_b = -credit_a # Debit To Account
        elif account_a.type == 'Pool' and account_b.type == 'User':
            credit_a = credit_a # Credit From Account
            credit_b = -credit_a # Debit To Account
        else:
            raise Exception("Cannot make transaction between account.type=='Pool' and account.type='Bank'")
        entry = cls(account_a=account_a, account_b=account_b, credit_a=credit_a, credit_b=credit_b, date=date, notes=notes)
        return entry

    def __str__(self):
        if self.credit_a >= 0 and self.credit_b >= 0:
            return '['+str(self.account_a)+' +'+str(self.credit_a)+']['+str(self.account_b)+' +'+str(self.credit_b)+']'
        if self.credit_a >= 0 and self.credit_b < 0:
            return '['+str(self.account_a)+' +'+str(self.credit_a)+']['+str(self.account_b)+' '+str(self.credit_b)+']'
        if self.credit_a < 0 and self.credit_b >= 0:
            return '['+str(self.account_a)+' '+str(self.credit_a)+']['+str(self.account_b)+' +'+str(self.credit_b)+']'
        if self.credit_a < 0 and self.credit_b < 0:
            return '['+str(self.account_a)+' '+str(self.credit_a)+']['+str(self.account_b)+' '+str(self.credit_b)+']'


class Transaction(models.Model):
    # Parents the Entry model, allowing Many-To-One Transactions across multiple accounts
    transaction_key = models.UUIDField(default=uuid.uuid4, editable=False)
    entry_set = models.ManyToManyField(Entry, blank=True, null=True)

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

class TransactionGroup(models.Model):
    # Holds multiple groups of Transaction objects, allowing single objects containing an entire set off accounts
    group_key = models.UUIDField(default=uuid.uuid4, editable=False)
    transaction_set = models.ManyToManyField(Transaction, blank=True, null=True)

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
