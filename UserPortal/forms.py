# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'bio', 'mailing_list', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')

class CustomUserChangeForm(UserCreationForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'bio', 'mailing_list', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')
