# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')

class CustomUserChangeForm(UserCreationForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
