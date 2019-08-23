from UserPortal.models import CustomUser
from django.db import models
from datetime import datetime
import uuid

TRANSACTION_TYPES = (
    ('Expense Claim', 'Expense Claim'), # A member claims the £35.66 they spent on petrol
    ('Charge', 'Charge'), # The club charges a member £39.00 for a meet
    ('Swap', 'Swap'), # Club members ggive each other money
    ('Reimbursement', 'Reimbursement'), # The club pays a member what they are owed OR a member pays the club what they owed
    ('Payment', 'Payment'), # The club pays a fee, for instance the deposit on a hut booking
    ('Purchase', 'Purchase'), # The club buys some gear
    ('Grant', 'Grant'), # The University gives the club a grant
    ('Uncategorised', 'Uncategorised'), # There is no suitable operation for this transaction
    ('Correctional', 'Correctional'), # The accounting system is out of line with the real world and the treasurer is correcting that
)

class Account(models.Model):
    account_key = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(CustomUser, blank=False, on_delete=models.PROTECT, related_name='bank_account') # Cannot delete user account if they have a bank account that exists
    is_virtual = models.BooleanField(default=True) # Allows tracking of virtual (user) vs real (actual physical account) account types without multiple models

    """
    balance = models.DecimalField(max_digits=7, decimal_places=2) # Cannot have more than 2dp for money values. Accounts can't go beyond +/- £99,999.99
    SHOULD BE LIVE-CALCULATED FROM TRANSACTIONS
    """
    def __str__(self):
        return str(self.owner)

class Transaction(models.Model):
    account = models.ForeignKey(Account, blank=False, on_delete=models.PROTECT) # Cannot delete an account if they have transactions that exist
    date = models.DateTimeField(blank=False, default=datetime.now) # When did the transaction occur?
    amount = models.DecimalField(max_digits=7, decimal_places=2, help_text='For a virtual account, a positive transaction is a credit. For a real account, a positive transaction is an increase in wealth.')
    """
    How much money went in/out of the account?

    For a virtual account:
    - a positive transaction represents a credit (they now owe the club less money than before)
    - a negative transaction represents a debit (they now owe the club more money than before)

    For a non-virtual account:
    - a positive transaction represents an increase in wealth (the club account now has more money in it)
    - a negative transaction represents a decrease in wealth (the club account now has more money in it)
    """
    category = models.CharField(max_length=50, choices=TRANSACTION_TYPES, blank=False)
    notes = models.TextField(blank=True) # Any notes about the transaction.
    approved = models.BooleanField(default=False) # Has the treasurer or other authorised person approved this transaction?
    def __str__(self):
        return '['+str(self.date)+']['+str(self.category)+'] '+str(self.account.owner)+': '+str(self.amount)

"""
    Example flow of transactions, assuming everyone involved started at £0.00

    1. The club recieves a grant of £500.00 from the university:
        account = Treasury
        date = 2019.08.22
        amount = 500.00
        category = 'grant'
        notes = 'University grant'
        approved = True
        balance_after_transaction = Treasury.balance = 500.00

    2. The club pays a £50.00 deposit on a hut booking:
        account = Treasury
        date = 2019.08.23
        amount = -50.00
        category = 'payment'
        notes = 'Hut booking deposit for upcoming caving meet'
        approved = True
        balance_after_transaction = Treasury.balance = 450.00

    3. People go caving, one of them pays the £45.00 remaining hut fee from their own pocket:
        account = GenerousMember
        date = 2019.08.25
        amount = 45.00
        category = 'expense_claim'
        notes = 'Paid hut fees on caving meet'
        approved = True
        balance_after_transaction = GenerousMember.balance = 45.00

    3. The meet leader logs the trip in the system, and charges everyone the £35.00 meet fee
        account = GenerousMember
        date = 2019.08.27
        amount = -35.00
        category = 'charge'
        notes = 'Charge from caving meet'
        approved = True
        balance_after_transaction = GenerousMember.balance = 10.00

    4. The club pay the member the oustanding £10.00 balance
        Transaction 1:
            account = Treasury
            date = 2019.08.29
            amount = -10.00
            category = 'reimbursement'
            notes = 'Paid outstanding balance'
            approved = True
            balance_after_transaction = Treasury.balance = 430.00
        Transaction 2:
            account = GenerousMember
            date = 2019.08.29
            amount = -10.00
            category = 'reimbursement'
            notes = 'Paid outstanding balance'
            approved = True
            balance_after_transaction = GenerousMember.balance = 0.00
        These two transactions would be created alongside a "TransactionPair," which ties particular fields together
"""

class TransactionPair(models.Model):
    # Ties two transactions together, useful when transactions are internal
    transaction_a = models.ForeignKey(Transaction, blank=False, related_name='transaction_a', null=True, on_delete=models.SET_NULL)
    transaction_b = models.ForeignKey(Transaction, blank=False, related_name='transaction_b', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '['+str(self.transaction_a.date)+']['+str(self.transaction_a.category)+'] From '+str(self.transaction_a.account.owner)+' To '+str(self.transaction_b.account.owner)+': '+str(self.transaction_a.amount)

    @classmethod
    def create(cls, account_a, account_b, date, amount, category, notes, approved=False):
        # Creates two transactions, and ties their dates, amounts, categories, notes, and approved status together. ORDER OF ACCOUNTS MATTERS!
        # "amount" represents how much money is going from one account to the other
        if account_a.is_virtual and account_b.is_virtual:
            # Virtual to Virtual, as in a member to member swap
            amount_a = amount # Credit account A
            amount_b = -amount # Debit account B
        elif account_a.is_virtual and not account_b.is_virtual:
            # Virtual to Real, as in a member pays their debt
            amount_a = amount # Credit account A
            amount_b = amount # Increase wealth of account B
        elif not account_a.is_virtual and account_b.is_virtual:
            # Real to Virtual, as in the club pays a member its debt
            amount_a = -amount # Decrease wealth of account A
            amount_b = -amount # Debit account B
        elif not account_a.is_virtual and not account_b.is_virtual:
            # Real to Real, as in the club transfers money between its own accounts
            amount_a = -amount # Decrease wealth of account A
            amount_b = amount # Increase wealth of account B
        TransactionA = Transaction(
            account = account_a,
            date = date,
            amount = amount_a,
            category = category,
            notes = '[Transaction Pair: ('+str(amount)+') From '+str(account_a.owner.full_name)+' ('+str(account_a.owner.username)+') To '+str(account_b.owner.full_name)+' ('+str(account_b.owner.username)+')]'+notes,
            approved = approved,
        )
        TransactionB = Transaction(
            account = account_b,
            date = date,
            amount = amount_b,
            category = category,
            notes = '[Transaction Pair: ('+str(amount)+') From '+account_a.owner.full_name+' ('+account_a.owner.username+') To '+account_b.owner.full_name+'('+account_b.owner.username+')]'+notes,
            approved = approved,
        )
        Pair = cls(transaction_a = TransactionA, transaction_b = TransactionB)
        return Pair
