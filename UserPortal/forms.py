# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    data_protection = forms.BooleanField(required=True)
    medical_data = forms.BooleanField(required=True)
    risk_acceptance = forms.BooleanField(required=True, label="Participation Statement")
    constituion = forms.BooleanField(required=True)
    mailing_list = forms.BooleanField(required=False, label="Subscribe to mailing list?", help_text='This is how most club business is conducted. It is highly recommended that you subscribe. If you are already subscribed and leave this box unchecked, you will be unsubscribed.')

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'mailing_list', 'phone_number', 'emergency_contact_name', 'emergency_phone_number', 'status', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')

class CustomUserChangeForm(UserCreationForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('__all__')

class EditUser(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'college', 'email', 'mailing_list', 'phone_number', 'emergency_contact_name', 'emergency_phone_number', 'status', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')

class SuperEditUser(forms.ModelForm):

    class Meta:
        widgets = {
            'rank': forms.CheckboxSelectMultiple,
            'groups': forms.CheckboxSelectMultiple,
            'user_permissions': forms.CheckboxSelectMultiple,
        }
        model = CustomUser
        fields = ('username', 'full_name', 'college', 'email', 'mailing_list', 'phone_number', 'emergency_contact_name', 'emergency_phone_number', 'status', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes', 'groups', 'rank', 'is_superuser', 'is_staff', 'is_human', 'user_permissions')
