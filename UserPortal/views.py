from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, Http404
from django.http import request
from datetime import datetime
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import *
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/SignUp.html'

    def form_valid(self, form):
        print("Form Valid")
        if form.cleaned_data['mailing_list']:
            # If user has checked the mailing list box, they get their full name and email added to the SubscribeQueue.txt file
            f = open("../SubscribeQueue.txt", "a")
            f.write('\"'+form.cleaned_data['full_name']+'\" <'+form.cleaned_data['email']+'>\n')
            f.close()
        else:
            # If user has NOT checked the mailing list box, they get their full name and email added to the UnubscribeQueue.txt file
            f = open("../UnsubscribeQueue.txt", "a")
            f.write(form.cleaned_data['email']+'\n')
            f.close()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditProfile(UpdateView):
    model = CustomUser
    success_url = reverse_lazy('UserPortalDashboard')
    template_name = 'registration/EditProfile.html'
    form_class = EditUser
    template_name_suffix = '_update_form'
    slug_field = 'user_key'

    def form_valid(self, form):
        print("Form Valid")
        if form.cleaned_data['mailing_list']:
            # If user has checked the mailing list box, they get their full name and email added to the SubscribeQueue.txt file
            f = open("../SubscribeQueue.txt", "a")
            f.write('\"'+form.cleaned_data['full_name']+'\" <'+form.cleaned_data['email']+'>\n')
            f.close()
        else:
            # If user has NOT checked the mailing list box, they get their full name and email added to the UnubscribeQueue.txt file
            f = open("../UnsubscribeQueue.txt", "a")
            f.write(form.cleaned_data['email']+'\n')
            f.close()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != self.request.user:
            raise Http404("You cannot edit someone else's profile")
        return super(EditProfile, self).dispatch(request, *args, **kwargs)

@method_decorator(permission_required('UserPortal.change_customuser'), name='dispatch')
class SuperEditProfile(UpdateView):
    model = CustomUser
    success_url = reverse_lazy('EditUsers')
    template_name = 'registration/EditProfile.html'
    form_class = SuperEditUser
    template_name_suffix = '_update_form'
    slug_field = 'user_key'

    def form_valid(self, form):
        print("Form Valid")
        if form.cleaned_data['mailing_list']:
            # If user has checked the mailing list box, they get their full name and email added to the SubscribeQueue.txt file
            f = open("../SubscribeQueue.txt", "a")
            f.write('\"'+form.cleaned_data['full_name']+'\" <'+form.cleaned_data['email']+'>\n')
            f.close()
        else:
            # If user has NOT checked the mailing list box, they get their full name and email added to the UnubscribeQueue.txt file
            f = open("../UnsubscribeQueue.txt", "a")
            f.write(form.cleaned_data['email']+'\n')
            f.close()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404("You must be a superuser to edit someone else's profile")
        return super(SuperEditProfile, self).dispatch(request, *args, **kwargs)

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

@method_decorator(login_required, name='dispatch')
class UserPortalDashboard(TemplateView):
    template_name = 'UserPortal/Dashboard.html'

@method_decorator(permission_required('UserPortal.change_customuser'), name='dispatch')
class EditUsers(ListView):
    model = CustomUser
    context_object_name = 'user_list'
    template_name = 'UserPortal/EditUsers.html'
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404("You must be a superuser to edit someone else's profile")
        return super(EditUsers, self).dispatch(request, *args, **kwargs)

@method_decorator(permission_required('UserPortal.add_committee'), name='dispatch')
class CommitteeAdd(CreateView):
    model = Committee
    template_name = 'UserPortal/CommitteeForm.html'
    success_url = reverse_lazy('ContactCommittee')
    fields = '__all__'

@method_decorator(permission_required('UserPortal.change_committee'), name='dispatch')
class CommitteeEdit(UpdateView):
    model = Committee
    template_name = 'UserPortal/CommitteeForm.html'
    success_url = reverse_lazy('ContactCommittee')
    fields = '__all__'

@method_decorator(permission_required('UserPortal.delete_committee'), name='dispatch')
class CommitteeDelete(DeleteView):
    model = Committee
    template_name = 'UserPortal/CommitteeForm.html'
    success_url = reverse_lazy('ContactCommittee')

@method_decorator(permission_required('UserPortal.add_rank'), name='dispatch')
class RankAdd(CreateView):
    model = Rank
    template_name = 'UserPortal/RankForm.html'
    success_url = reverse_lazy('UserPortalDashboard')
    fields = '__all__'

@method_decorator(permission_required('UserPortal.change_rank'), name='dispatch')
class RankEdit(UpdateView):
    model = Rank
    template_name = 'UserPortal/RankForm.html'
    success_url = reverse_lazy('UserPortalDashboard')
    fields = '__all__'

@method_decorator(permission_required('UserPortal.delete_rank'), name='dispatch')
class RankDelete(DeleteView):
    model = Rank
    template_name = 'UserPortal/RankForm.html'
    success_url = reverse_lazy('UserPortalDashboard')
