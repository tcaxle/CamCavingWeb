from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from UserPortal.models import CustomUser
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

class GearFirstAid(TemplateView):
    template_name = 'Gear/FirstAid.html'
class GearTape(ListView):
    model = CustomUser
    template_name = 'Gear/Tape.html'
    queryset = CustomUser.objects.all().order_by('full_name')
    context_object_name = 'user_list'

@method_decorator(permission_required('Gear.view_hires'), name='dispatch')
class ViewHiresRope(ListView):
    model = HireRope
    context_object_name = 'hires_list'
    template_name = 'Gear/ViewHires.html'
    queryset = HireRope.objects.all().order_by('-signed_out')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditRope(UpdateView):
    model = Rope
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteRope(DeleteView):
    model = Rope
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddRope(CreateView):
    model = Rope
    template_name = 'Gear/AddForm.html'
    fields = '__all__'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditHelmet(UpdateView):
    model = Helmet
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteHelmet(DeleteView):
    model = Helmet
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddHelmet(CreateView):
    model = Helmet
    template_name = 'Gear/AddForm.html'
    fields = '__all__'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditSRTKit(UpdateView):
    model = SRTKit
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteSRTKit(DeleteView):
    model = SRTKit
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddSRTKit(CreateView):
    model = SRTKit
    template_name = 'Gear/AddForm.html'
    fields = '__all__'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditHarness(UpdateView):
    model = Harness
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteHarness(DeleteView):
    model = Harness
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddHarness(CreateView):
    model = Harness
    template_name = 'Gear/AddForm.html'
    fields = '__all__'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditUndersuit(UpdateView):
    model = Undersuit
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteUndersuit(DeleteView):
    model = Undersuit
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddUndersuit(CreateView):
    model = Undersuit
    template_name = 'Gear/AddForm.html'
    fields = '__all__'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditOversuit(UpdateView):
    model = Oversuit
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteOversuit(DeleteView):
    model = Oversuit
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddOversuit(CreateView):
    model = Oversuit
    template_name = 'Gear/AddForm.html'
    fields = '__all__'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class EditOtherGear(UpdateView):
    model = OtherGear
    template_name = 'Gear/EditForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('GearHire')
    fields = '__all__'

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class DeleteOtherGear(DeleteView):
    model = OtherGear
    template_name = 'Gear/DeleteForm.html'
    success_url = reverse_lazy('GearHire')

@method_decorator(permission_required('Gear.register_gear'), name='dispatch')
class AddOtherGear(CreateView):
    model = OtherGear
    template_name = 'Gear/AddForm.html'
    fields = ['name', 'quantity', 'on_loan', 'notes']
    success_url = reverse_lazy('GearHire')
    def form_valid(self, form):
        form.instance.available = form.instance.quantity - form.instance.on_loan
        return super().form_valid(form)

class GearHire(TemplateView):
    template_name = 'Gear/Hire.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_list'] = CustomUser.objects.all()

        context['rope_list'] = Rope.objects.all()
        context['hirerope_list'] = HireRope.objects.filter(open=True)

        context['helmet_list'] = Helmet.objects.all()
        context['hirehelmet_list'] = HireHelmet.objects.filter(open=True)

        context['srtkit_list'] = SRTKit.objects.all()
        context['hiresrtkit_list'] = HireSRTKit.objects.filter(open=True)

        context['harness_list'] = Harness.objects.all()
        context['hireharness_list'] = HireHarness.objects.filter(open=True)

        context['undersuit_list'] = Undersuit.objects.all()
        context['hireundersuit_list'] = HireUndersuit.objects.filter(open=True)

        context['oversuit_list'] = Oversuit.objects.all()
        context['hireoversuit_list'] = HireOversuit.objects.filter(open=True)

        context['othergear_list'] = OtherGear.objects.all()
        return context

# Signing in and out views as redirects that create and edit HireInstance Models

# Rope
def RopeSignOut(request, pk):
    if request.method == 'POST':
        rope = get_object_or_404(Rope, pk=pk, available=True)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        HireInstance = HireRope(rope=rope, signed_out_by=user)
        rope.available = False
        HireInstance.save()
        rope.save()
    return redirect('GearHire')

def RopeSignIn(request, pk):
    rope = get_object_or_404(Rope, pk=pk, available=False)
    HireInstance = get_object_or_404(HireRope, rope=rope, signed_in=None)
    rope.available = True
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.open = False
    HireInstance.save()
    rope.save()
    return redirect('GearHire')

# Helmets
def HelmetSignOut(request, pk):
    if request.method == 'POST':
        helmet = get_object_or_404(Helmet, pk=pk, available=True)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        HireInstance = HireHelmet(helmet=helmet, signed_out_by=user)
        helmet.available = False
        HireInstance.save()
        helmet.save()
    return redirect('GearHire')

def HelmetSignIn(request, pk):
    helmet = get_object_or_404(Helmet, pk=pk, available=False)
    HireInstance = get_object_or_404(HireHelmet, helmet=helmet, signed_in=None)
    helmet.available = True
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.open = False
    HireInstance.save()
    helmet.save()
    return redirect('GearHire')

# SRT Kits
def SRTKitSignOut(request, pk):
    if request.method == 'POST':
        kit = get_object_or_404(SRTKit, pk=pk, available=True)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        HireInstance = HireSRTKit(kit=kit, signed_out_by=user)
        kit.available = False
        HireInstance.save()
        kit.save()
    return redirect('GearHire')

def SRTKitSignIn(request, pk):
    kit = get_object_or_404(SRTKit, pk=pk, available=False)
    HireInstance = get_object_or_404(HireSRTKit, kit=kit, signed_in=None)
    kit.available = True
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.open = False
    HireInstance.save()
    kit.save()
    return redirect('GearHire')

# Harnesses
def HarnessSignOut(request, pk):
    if request.method == 'POST':
        harness = get_object_or_404(Harness, pk=pk, available=True)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        HireInstance = HireHarness(harness=harness, signed_out_by=user)
        harness.available = False
        HireInstance.save()
        harness.save()
    return redirect('GearHire')

def HarnessSignIn(request, pk):
    harness = get_object_or_404(Harness, pk=pk, available=False)
    HireInstance = get_object_or_404(HireHarness, harness=harness, signed_in=None)
    harness.available = True
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.open = False
    HireInstance.save()
    harness.save()
    return redirect('GearHire')

# Undersuits
def UndersuitSignOut(request, pk):
    if request.method == 'POST':
        undersuit = get_object_or_404(Undersuit, pk=pk, available=True)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        HireInstance = HireUndersuit(undersuit=undersuit, signed_out_by=user)
        undersuit.available = False
        HireInstance.save()
        undersuit.save()
    return redirect('GearHire')

def UndersuitSignIn(request, pk):
    undersuit = get_object_or_404(Undersuit, pk=pk, available=False)
    HireInstance = get_object_or_404(HireUndersuit, undersuit=undersuit, signed_in=None)
    undersuit.available = True
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.open = False
    HireInstance.save()
    undersuit.save()
    return redirect('GearHire')

# Oversuits
def OversuitSignOut(request, pk):
    if request.method == 'POST':
        oversuit = get_object_or_404(Oversuit, pk=pk, available=True)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        HireInstance = HireOversuit(oversuit=oversuit, signed_out_by=user)
        oversuit.available = False
        HireInstance.save()
        oversuit.save()
    return redirect('GearHire')

def OversuitSignIn(request, pk):
    oversuit = get_object_or_404(Oversuit, pk=pk, available=False)
    HireInstance = get_object_or_404(HireOversuit, oversuit=oversuit, signed_in=None)
    oversuit.available = True
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.open = False
    HireInstance.save()
    oversuit.save()
    return redirect('GearHire')

# Other Gear
def OtherGearSignOut(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST['amount'])
        gear = get_object_or_404(OtherGear, pk=pk)
        user = get_object_or_404(CustomUser, username=request.POST['user'])
        SignOutInstance = SignOutOtherGear(gear=gear, signed_out_by=user, quantity=quantity)
        gear.on_loan += quantity
        gear.available -= quantity
        SignOutInstance.save()
        gear.save()
    return redirect('GearHire')

def OtherGearSignIn(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST['amount'])
        gear = get_object_or_404(OtherGear, pk=pk)
        SignInInstance = SignInOtherGear(gear=gear, signed_in_by=request.user, quantity=quantity)
        gear.on_loan -= quantity
        gear.available += quantity
        SignInInstance.save()
        gear.save()
    return redirect('GearHire')
