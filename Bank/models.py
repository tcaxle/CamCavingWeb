from UserPortal.models import CustomUser
from django.db import models
from datetime import datetime
import uuid

class Account(models.Model):
    # Representitive of legal entities. This could be the actual club account, a retailer that the club purchases from, or a member of the club
    # METADATA:
    sort_name = models.CharField(max_length=100, blank=False, editable=False, default='-')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    # DATA:
    owner = models.OneToOneField(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='bank_account', help_text='If account is to be owned by a person, please select that user here.')
    name = models.CharField(max_length=100, blank=True, help_text='If account is unowned, please give it a sensible name.')
    ACCOUNT_TYPES = (
        ('Bank', 'Bank'),
        ('User', 'User'),
        ('Pool', 'Pool')
    )
    type = models.CharField(max_length=100, blank=False, choices=ACCOUNT_TYPES)

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

class CustomCurrencyCredit(models.Model):
    # Holds the value and date of said value of a currency
    credit = models.DecimalField(max_digits=7, decimal_places=2, blank=False, help_text='The value of this currency in GBP. For a currency that will be a debit (charge), enter a negative number. For a currency that will be a credit, enter a positive number.') # "Rate" of currency; the amount to credit an account by per unit
    date = models.DateTimeField(blank=False, default=datetime.now)
    custom_currency = models.ForeignKey(CustomCurrency, on_delete=models.PROTECT, blank=False, null=False, editable=False, related_name='credit_set')

class CustomCurrency(models.Model):
    # Allows custom "currencies," which are rates to be charged
    # CustomCurrencies can only be credited to users, and always debit a pool (negative credits for a charge)
    # the value of

    # METADATA:
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    # DATA:
    name = models.CharField(max_length=100, blank=False)
    pool = models.ForeignKey(Account, blank=False, null=False, on_delete=models.PROTECT) # The pool to be debited when someone is credited with this currency

    def get_credit(self, date=datetime.now()):
        # returns the credit of the currency at a given date
        credit = self.credit_set.exclude(date__gt=date).order_by('-date')[0]

    def __str__(self):
        return self.name

class CustomExpense(models.Model):
    # Allows custom "expenses," which are descriptive psuedonyms forr pools
    # CustomExpenses can only be credited to users, and always debit a pool (negative credits for a charge)

    # METADATA:
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    # DATA:
    name = models.CharField(max_length=100, blank=False)
    pool = models.ForeignKey(Account, blank=False, null=False, on_delete=models.PROTECT) # The pool to be debited when someone is credited with this expense

    def __str__(self):
        return self.name

class CommonData(models.Model):
    # Data that is the same for a collection of financial objects

    # Created:
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT, related_name='created_transaction_group_set') # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False)

    # Approved:
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(CustomUser, blank=True, null=True, editable=False, on_delete = models.PROTECT, related_name='approved_transaction_group_set', default=None) # Who approved the object
    approved_on = models.DateTimeField(blank=True, null=True, default=datetime.now, editable=False) # When was the object approved?

    # Date:
    date = models.DateTimeField(blank=False, default=datetime.now)

    # Locked:
    is_locked = models.BooleanField(default=False, editable=False)

class FinancialObject(models.Model):
    # meta-model for financial objects comtaining shared fields (whose values differ from object to object)

    # UUID:
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    # Name:
    name = models.CharField(max_length=100, blank=False)

    # Notes:
    notes = models.TextField(blank=True)

    # Editable:
    is_editable = models.BooleanField(default=False, editable=False)

    # Common Data:
    common_data = models.ForeignKey(CommonData, on_delete=models.PROTECT, related_name='object_set')

    class Meta:
        abstract = True

class TransactionGroup(FinancialObject):
    # Held by multiple Transaction objects, allowing single objects containing an entire set off accounts \
    # Holds a list of creditors and debtors, the transaction set is subsequently the orthogonal mapping of these two lists

    # Setup
    creditors = models.ManyToManyField(Account, blank=False, related_name="transaction_group_creditor_set") # Accounts to be credited
    debtors = models.ManyToManyField(Account, blank=False, related_name="transaction_group_debtor_set") # Accounts to be debited

    def SetApprove(self, by=None, on=None, status=False):
        if status:
            self.common_data.is_approved = True
            self.common_data.approved_by = by
            self.common_data.approved_on = on
        else:
            self.common_data.is_approved = False
            self.common_data.approved_by = None
            self.common_data.approved_on = None
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on, status=True)

    def populate(self, t_g_list):
        # takes a list of tuples: [(creditor, debtor, amount, currency, expense), ...] \
        # iterates over it, and updates the transaction group accordingly
        # currency and expense must be included or None if not relevant

        # iterate over list of tuples
        for creditor, debtor, amount, currency, expense in t_g_list:
            # add creditor to creditor list
            self.creditors.add(creditor)
            self.debtors.add(debtor)
            # iterate over dictionary
            # create a transaction, inherit the common data, and associate it with this group.
            if currency is None and expense is None:
                # normal transaction
                transaction = Transaction.create_normal(
                    account_a=creditor,
                    account_b=debtor,
                    credit_a=Decimal(amount),
                    common_data=self.common_data,
                    )
            elif currency is None and expense is not None:
                # custom expense transaction
                transaction = Transaction.create_expense(
                    account_a=creditor,
                    account_b=debtor,
                    credit_a=Decimal(amount),
                    common_data=self.common_data,
                    custom_expense=expense,
                    )
            elif currency is not None and expense is None:
                # custom currency transaction
                transaction = Transaction.create_currency(
                    account_a=creditor,
                    account_b=debtor,
                    common_data=self.common_data,
                    custom_currency=currency,
                    currency_quantity=int(amount),
                    )
            # set the name
            transaction.name = str(debtor) + ' -> ' + str(creditor)
            # save it!
            transaction.save()

    def repopulate(self, t_g_list):
        # takes a list of tuples: [(creditor, debtor, amount, currency, expense), ...] \
        # iterates over it, and updates the transaction group accordingly
        # currency and expense must be included or None if not relevant

        # List of old transactions
        working_set = self.transaction_set.all()

        # editing and creating:
        for creditor, debtor, amount, currency, expense in t_g_list:
            # check for matching transaction in group:
            if self.transaction_set.get(account_a=creditor, account_b=debtor, custom_currency=currency, custom_expense=expense).exists():
                ## EDIT pairs that are in both old and new ##
                # retrieve
                transaction = self.transaction_set.get(account_a=creditor, account_b=debtor, custom_currency=currency, custom_expense=expense)
                # edit amount
                if transaction.type != "Custom Currency":
                    # normal or expense type transaction
                    transaction.credit_a = Decimal(amount)
                else:
                    # currency type transaction
                    # set the quantity
                    transaction.currency_quantity = int(amount)
                    # calculate and set the credit
                    transaction.credit_a = int(amount)*custom_currency.get_credit(self.common_data.date)
                # set the name
                transaction.name = str(debtor) + ' -> ' + str(creditor)
                # save it!
                transaction.save()
                # remove from working set
                working_set.remove(transaction)
            else:
                ## NEW transactions for pairs in new but not old ##
                # create a transaction, inherit the common data, and associate it with this group.
                if currency is None and expense is None:
                    # normal transaction
                    transaction = Transaction.create_normal(
                        account_a=creditor,
                        account_b=debtor,
                        credit_a=Decimal(amount),
                        common_data=self.common_data,
                        )
                elif currency is not None and expense is not None:
                    # don't allow transactions that are both an expense and a currency
                    break
                elif expense is not None:
                    # custom expense transaction
                    transaction = Transaction.create_expense(
                        account_a=creditor,
                        account_b=debtor,
                        credit_a=Decimal(amount),
                        common_data=self.common_data,
                        custom_expense=expense,
                        )
                elif currency is not None:
                    # custom currency transaction
                    transaction = Transaction.create_currency(
                        account_a=creditor,
                        account_b=debtor,
                        common_data=self.common_data,
                        custom_currency=currency,
                        currency_quantity=int(amount),
                        )
                # set the name
                transaction.name = str(debtor) + ' -> ' + str(creditor)
                # save it!
                transaction.save()

        ## DELETE transactions left in working set ##
        for transaction in working_set:
            transaction.delete()

        # rebuild creditor and debtor lists:
        self.creditors.clear()
        self.debtors.clear()
        for transaction in self.transaction_set:
            self.creditors.add(transaction.account_a)
            self.debtors.add(transaction.account_b)

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
        return 'Transaction Group: '+self.name

    class Meta:
        permissions = [
            ("approve__transactiongroup", "Can approve transaction groups"),
            ("lock__transactiongroup", "Can lock transaction groups"),
        ]

class Transaction(FinancialObject):
    # Atomic unit of dataset, represents a one-to-one transaction

    # SETUP:
    account_a = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT, related_name='transaction_set_a')
    account_b = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT, related_name='transaction_set_b')

    # DATA:
    credit_a = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # Amount that account a has been credited by
    credit_b = models.DecimalField(max_digits=7, decimal_places=2, blank=False) # Amount that account b has been credited by

    # METADATA:

    # transaction types
    TRANSACTION_TYPES = (
        ('Normal', 'Normal'),
        ('Custom Currency', 'Custom Currency'),
        ('Custom Expense', 'Custom Expense')
    )
    type = models.CharField(max_length=100, blank=False, choices=ACCOUNT_TYPES)

    # Custom Currency Handling:
    custom_currency = models.ForeignKey(CustomCurrency, on_delete=models.PROTECT, blank=True, null=True, editable=False, default=None)
    currency_quantity = models.IntegerField(blank=True, null=True, editable=False, default=None)

    # Custom Expense Handling:
    custom_expense = models.ForeignKey(CustomExpense, on_delete=models.PROTECT, blank=True, null=True, editable=False, default=None)

    # Transaction Groups:
    transaction_group = models.ForeignKey(TransactionGroup, on_delete=models.CASCADE, blank=True, null=True, editable=False, default=None)

    def save(self, *args, **kwargs):
        self.date = datetime(self.date.year, self.date.month, self.date.day, 12, 0, 0)
        if (self.account_a.type == 'Bank' and self.account_b.type != 'Bank') or(self.account_a.type != 'Bank' and self.account_b.type == 'Bank'):
            # check if transaction is between bank and not a bank \
            # and credit both
            self.credit_a = self.credit_a # Credit Account A
            self.credit_b = self.credit_a # Credit Account B
        else:
            # else credit one and debit other
            self.credit_a = self.credit_a # Credit Account A
            self.credit_b = -self.credit_a # Debit Account B
        super().save(*args, **kwargs)

    @classmethod
    def create_normal(cls, account_a, account_b, credit_a, common_data):
        # creates a normal type transaction
        return cls(
            account_a=account_a,
            account_b=account_b,
            credit_a=credit_a,
            common_data=common_data,
            type="normal",
            )

    @classmethod
    def create_expense(cls, account_a, account_b, credit_a, common_data, custom_expense):
        # creates an expense type transaction
        return cls(
            account_a=account_a,
            account_b=account_b,
            credit_a=credit_a,
            common_data=common_data,
            type="Custom Expense",
            custom_expense=custom_expense,
            )

    @classmethod
    def create_expense(cls, account_a, account_b, common_data, custom_currency, currency_quantity):
        # creates a currency type transaction \
        # credit is calculated from currency, date of transaction, and quantity of currency
        return cls(
            account_a=account_a,
            account_b=account_b,
            common_data=common_data,
            type="Custom Currency",
            custom_currency=custom_currency,
            currency_quantity=currency_quantity,
            credit_a=currency_quantity*custom_currency.get_credit(common_data.date),
            )

    def SetApprove(self, by=None, on=None, status=False):
        if status:
            self.common_data.is_approved = True
            self.common_data.pproved_by = by
            self.common_data.pproved_on = on
        else:
            self.common_data.is_approved = False
            self.common_data.approved_by = None
            self.common_data.approved_on = None
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on, status=True)

    def __str__(self):
        return 'Transaction '+str(self.pk)

    class Meta:
        permissions = [
            ("approve__transaction", "Can approve transactions"),
        ]

"""
class Entry(models.Model):
    # The smallest unit of the transation family. Records an individual double-entry transaction
    entry_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(CustomUser, blank=False, null=True, editable=False, on_delete=models.PROTECT) # Who created the object
    created_on = models.DateTimeField(blank=False, default=datetime.now, editable=False) # When was the object created?
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    notes = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False, editable=False)
    transaction = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.PROTECT)
    is_editable = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(CustomUser, blank=True, null=True, editable=False, on_delete = models.PROTECT, related_name='approved_entry_set') # Who approved the object
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
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on)


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
"""

class FeeTemplate(models.Model):
    # A set of currencies to provide the flesh of an Event model
    template_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    custom_currency = models.ManyToManyField(CustomCurrency, blank=True) # Custom currencies that can be credited to users
    custom_expense = models.ManyToManyField(CustomExpense, blank=True) # Pools that can be directly debited

    def __str__(self):
        return self.name

class Event(FinancialObject):
    # A wrapper for the TransactionGroup that integrates custom currecies \
    # to make doing the accounts for an event (a meet, a dinner, etc.) easier
    transaction_group = models.OneToOneField(TransactionGroup, blank=True, null=True, on_delete=models.CASCADE, related_name='event') # The transaction group tied to the event
    # Fee Templates:
    fee_template = models.ForeignKey(FeeTemplate, blank=False, null=True, on_delete=models.PROTECT)
    # Name
    name = models.CharField(max_length=100, blank=False)
    # Creditors

    def SetApprove(self, by=None, on=None, status=False):
        if status:
            self.common_data.is_approved = True
            self.common_data.approved_by = by
            self.common_data.approved_on = on
        else:
            self.common_data.is_approved = False
            self.common_data.approved_by = None
            self.common_data.approved_on = None
        self.save()

    def ToggleApprove(self, by, on):
        if self.is_approved:
            self.SetApprove(status=False)
        else:
            self.SetApprove(by, on, status=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("approve__event", "Can approve events"),
        ]
