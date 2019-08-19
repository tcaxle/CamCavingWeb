# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    data_protection = forms.BooleanField(required=True)
    medical_data = forms.BooleanField(required=True)
    risk_acceptance = forms.BooleanField(required=True, label="Participation Statement")
    constituion = forms.BooleanField(required=True)
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'phone_number', 'emergency_contact_name', 'emergency_phone_number', 'status', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')

class CustomUserChangeForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'status', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')
