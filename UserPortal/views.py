from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser

def username_check(user):
    return user.email.endswith('@example.com')

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/SignUp.html'

class EditProfile(UpdateView):
    model = CustomUser
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'registration/EditProfile.html'
    fields = ['full_name', 'email', 'bio', 'tape_colour_1', 'tape_colour_2', 'tape_colour_3', 'tape_colour_notes']
    template_name_suffix = '_update_form'
    slug_field = 'user_key'

@login_required(login_url='/Portal/login/')
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('ChangePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/ChangePassword.html', {
        'form': form
    })

@login_required(login_url='/Portal/login/')
def UserPortalDashboard(request):
    return render(request, 'UserPortal/Dashboard.html')
