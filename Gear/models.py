from UserPortal.models import CustomUser
from django.db import models
from django.utils import timezone

class HireSupport(models.Model):

    class Meta:
        managed = False  # No database table creation or deletion operations will be performed for this model.
        permissions = [
            ("hire_self", "Can hire gear on their own behalf"),
            ("hire_other", "Can hire gear on behalf of others"),
        ]

# Rope
class Rope(models.Model):
    purchased_year = models.IntegerField(blank=False)
    diameter = models.IntegerField(verbose_name='Diameter (mm)', blank=False)
    length = models.IntegerField(verbose_name='Length (m)', blank=False)
    notes = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)+': '+str(self.purchased_year)+' - '+str(self.length)+'m'+str(self.diameter)+'mm'

class HireRope(models.Model):
    rope = models.ForeignKey(Rope, blank=False, on_delete=models.CASCADE)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE, related_name='%(class) signed_out')
    signed_in_by = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)
    signed_in = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.rope)+' - '+str(self.signed_out)

# Helmet
class Helmet(models.Model):
    purchased_year = models.IntegerField(blank=False)
    uid = models.IntegerField(blank=False, verbose_name='UID')
    notes = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uid)+': '+str(self.purchased_year)

class HireHelmet(models.Model):
    helmet = models.ForeignKey(Helmet, blank=False, on_delete=models.CASCADE)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE, related_name='%(class) signed_out')
    signed_in_by = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)
    signed_in = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.helmet)+' - '+str(self.signed_out)

# SRT Kit
class SRTKit(models.Model):
    colour_code = models.CharField(max_length=50, blank=False, default='Purple & ')
    notes = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.colour_code

class HireSRTKit(models.Model):
    kit = models.ForeignKey(SRTKit, blank=False, on_delete=models.CASCADE)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE, related_name='%(class) signed_out')
    signed_in_by = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)
    signed_in = models.DateTimeField(blank=True, null=True)#
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.kit)+' - '+str(self.signed_out)

# Harness
class Harness(models.Model):
    purchased_year = models.IntegerField(blank=False)
    uid = models.IntegerField(blank=False, verbose_name='UID')
    notes = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uid)+': '+str(self.purchased_year)

class HireHarness(models.Model):
    harness = models.ForeignKey(Harness, blank=False, on_delete=models.CASCADE)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE, related_name='%(class) signed_out')
    signed_in_by = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)
    signed_in = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.harness)+' - '+str(self.signed_out)

# Undersuits
class Undersuit(models.Model):
    uid = models.IntegerField(blank=False, verbose_name='UID')
    size = models.CharField(max_length=1, blank=False)
    notes = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uid)+': '+self.size

class HireUndersuit(models.Model):
    undersuit = models.ForeignKey(Undersuit, blank=False, on_delete=models.CASCADE)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE, related_name='%(class) signed_out')
    signed_in_by = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)
    signed_in = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.undersuit)+' - '+str(self.signed_out)

# Oversuits
class Oversuit(models.Model):
    uid = models.IntegerField(blank=False, verbose_name='UID')
    size = models.CharField(max_length=1, blank=False)
    notes = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uid)+': '+self.size

class HireOversuit(models.Model):
    oversuit = models.ForeignKey(Oversuit, blank=False, on_delete=models.CASCADE)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE, related_name='%(class) signed_out')
    signed_in_by = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)
    signed_in = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.oversuit)+' - '+str(self.signed_out)

# Other Gear
class OtherGear(models.Model):
    name = models.CharField(max_length=50, blank=False)
    quantity = models.IntegerField(blank=False)
    notes = models.TextField(blank=True)
    on_loan = models.IntegerField(blank=False, default=0)
    available = models.IntegerField(blank=False, default=quantity)

    def __str__(self):
        return self.name+' ('+str(self.quantity)+')'

class SignOutOtherGear(models.Model):
    gear = models.ForeignKey(OtherGear, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    signed_out_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)
    signed_out = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return str(self.gear)+' ('+str(self.quantity)+')'+' - '+str(self.signed_out)

class SignInOtherGear(models.Model):
    gear = models.ForeignKey(OtherGear, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    signed_in_by = models.ForeignKey(CustomUser, blank=False, on_delete=models.CASCADE)
    signed_in = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return str(self.gear)+' ('+str(self.quantity)+')'+' - '+str(self.signed_in)
