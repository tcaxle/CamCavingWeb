from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from UserPortal.models import CustomUser
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

class GearFirstAid(TemplateView):
    template_name = 'Gear/FirstAid.html'
class GearInventory(TemplateView):
    template_name = 'Gear/Inventory.html'
class GearTape(ListView):
    model = CustomUser
    template_name = 'Gear/Tape.html'
    queryset = CustomUser.objects.all().order_by('full_name')
    context_object_name = 'user_list'
class GearHire(TemplateView):
    template_name = 'Gear/Hire.html'

# Signing in and out views as redirects that create and edit HireInstance Models
def RopeSignOut(request, pk):
    rope = get_object_or_404(Rope, pk=pk, available=True)
    rope.available = False
    HireInstance = HireRope(rope=rope, signed_out_by=request.user)
    HireInstance.save()
    rope.save()
    return redirect('GearHire')

def RopeSignIn(request, pk):
    rope = get_object_or_404(Rope, pk=pk, available=False)
    rope.available = True
    HireInstance = get_object_or_404(HireRope, rope=rope, signed_in=None)
    HireInstance.signed_in_by = request.user
    HireInstance.signed_in = timezone.now()
    HireInstance.save()
    rope.save()
    return redirect('GearHire')
