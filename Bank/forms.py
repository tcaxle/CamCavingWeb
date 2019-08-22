from django import forms
from .models import *

class AddTransaction(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'date', 'amount', 'category', 'notes')

class SuperAddTransaction(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'date', 'amount', 'category', 'notes', 'approved')
