from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CreateEntry(forms.Form):
    creditor = forms.ModelChoiceField(label='Creditor', required=True, queryset=Account.objects.all().order_by('type'), help_text='The first party in the transaction entry.')
    debtor = forms.ModelChoiceField(label='Debtor', required=True, queryset=Account.objects.all().order_by('type'), help_text='The second party in the transaction entry.')
    amount = forms.DecimalField(label='Credit', max_digits=7, decimal_places=2, required=True, help_text="The amount to credit the first account. The matching credit/debit to the second account will be automatically generated.")
    date = forms.DateTimeField(widget=forms.SelectDateWidget, initial=datetime.now, help_text='The date on which the transaction occurred.')
    notes = forms.CharField(widget=forms.Textarea, required=False, help_text='Any useful details about the transaction. Be concise.')

    def clean(self):
        cleaned_data = super().clean()
        creditor = self.cleaned_data['creditor']
        debtor = self.cleaned_data['debtor']
        if (creditor.type == 'Bank' and debtor.type == 'Pool') or (creditor.type == 'Pool' and debtor.type == 'Bank'):
            raise forms.ValidationError('Cannot perform transaction between Bank and Pool account types.')

class CreateTransactionGroup(forms.Form):
    # A form to create a transaction group in the most generic way
    pass

class EditTransactionGroup(forms.Form):
    # A form to edit a transaction group in the most generic way
    pass

class ApproveTransactionGroup(forms.Form):
    # A form to allow the treasurer to make edits to and approve a transaction group
    pass
