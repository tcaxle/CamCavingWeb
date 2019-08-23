from django import forms
from .models import *

class AddTransaction(forms.ModelForm):
    amount = forms.DecimalField(max_digits=7, decimal_places=2, initial=0.00, help_text='For a virtual account, a positive transaction is a credit. For a real account, a positive transaction is an increase in wealth.')
    class Meta:
        widgets = {
            'date': forms.SelectDateWidget,
        }
        model = Transaction
        fields = ('account', 'date', 'amount', 'category', 'notes')

class SuperAddTransaction(forms.ModelForm):
    amount = forms.DecimalField(max_digits=7, decimal_places=2, initial=0.00, help_text='For a virtual account, a positive transaction is a credit. For a real account, a positive transaction is an increase in wealth.')
    class Meta:
        widgets = {
            'date': forms.SelectDateWidget,
        }
        model = Transaction
        fields = ('account', 'date', 'amount', 'category', 'notes', 'approved')

class AddTransactionPair(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), help_text='The account you are transfering from')
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), help_text='The account you are transfering to')
    amount = forms.DecimalField(max_digits=7, decimal_places=2, initial=0.00, help_text='The amount you are transfering in GBP')
    date = forms.DateTimeField(widget=forms.SelectDateWidget, initial=datetime.now, help_text='When the transaction occured')
    category = forms.ChoiceField(choices=TRANSACTION_TYPES)
    notes = forms.CharField(widget=forms.Textarea, required=False)

class SuperAddTransactionPair(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), help_text='The account you are transfering from')
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), help_text='The account you are transfering to')
    amount = forms.DecimalField(max_digits=7, decimal_places=2, initial=0.00, help_text='The amount you are transfering in GBP')
    date = forms.DateTimeField(widget=forms.SelectDateWidget, initial=datetime.now, help_text='When the transaction occured')
    category = forms.ChoiceField(choices=TRANSACTION_TYPES)
    notes = forms.CharField(widget=forms.Textarea, required=False)
    approved = forms.BooleanField(help_text='Transaction approved by treasurer?', required=False)
