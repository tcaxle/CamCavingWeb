from UserPortal.models import CustomUser
from django.db import models

class Rope(models.Model):
    diameter = models.IntegerField(max_length=10, label='Diameter (mm)', blank=False)
    length = models.IntegerField(max_length=10, label='Length (m)', blank=False)
    notes = models.TextField(blank=True)
    purchased_year = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.pk)+': 'str(self.purchased_year)+' - '+str(self.length)+'m'+str(self.diameter)+'mm'
