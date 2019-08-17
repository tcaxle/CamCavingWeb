# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('full_name', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes')}),
    )
    list_display = ['username', 'full_name', 'email', 'bio']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Rank)
admin.site.register(LegacyUser)
admin.site.register(Committee)
