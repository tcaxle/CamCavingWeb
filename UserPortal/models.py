from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid

COLOR_CHOICES = (
    ('black','BLACK'),
    ('brown', 'BROWN'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('yellow', 'YELLOW'),
    ('green', 'GREEN'),
    ('blue', 'BLUE'),
    ('purple', 'PURPLE'),
    ('grey', 'GREY'),
    ('white', 'WHITE'),
    ('earth', 'EARTH'),
    ('other', 'OTHER')
)

STATUS_CHOICES = (
    ('Frequent', 'Active - Frequent'),
    ('Infrequent', 'Active - Infrequent'),
    ('Expo', 'Active - Expo'),
    ('Inactive', 'Inactive'),
)

class Rank(models.Model):
    name = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=500, blank=True)
    email = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    user_key = models.UUIDField(default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50, blank=False)
    college = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    tape_colour_1 = models.CharField(verbose_name='Gear Tape Colour 1', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_2 = models.CharField(verbose_name='Gear Tape Colour 2', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_3 = models.CharField(verbose_name='Gear Tape Colour 3', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_notes = models.CharField(verbose_name='Gear Tape Notes', max_length=50, blank=True)
    mailing_list = models.BooleanField(verbose_name='Subscribe to Mailing List?', blank=False, default=False, help_text='This is how most club business is conducted. It is highly recommended that you subscribe. If you are already subscribed and leave this box unchecked, you will be unsubscribed.')
    rank = models.ManyToManyField(Rank, verbose_name='Club Position', blank=True, null=True)
    status = models.CharField(verbose_name='Status', max_length=20, choices=STATUS_CHOICES, blank=False, default='Inactive')
    phone_number = models.CharField(max_length=20, blank=True, help_text="See information below on use of emergency contact information.")
    emergency_phone_number = models.CharField(max_length=20, blank=True, help_text="See information below on use of emergency contact information.")
    emergency_contact_name = models.CharField(max_length=50, blank=True, help_text="See information below on use of emergency contact information.")
    is_human = models.BooleanField(default=True)

    def rank_display(self):
        return ', '.join([i.name for i in self.rank.all()])
    rank_display.short_description = 'Rank Display'

    def name(self):
        return self.full_name

    def __str__(self):
        return self.username

class Committee(models.Model):
    year = models.IntegerField()
    president = models.CharField(max_length=40, blank=True)
    senior_treasurer = models.CharField(max_length=40, blank=True)
    junior_treasurer = models.CharField(max_length=40, blank=True)
    secretary = models.CharField(max_length=40, blank=True)
    tackle_master = models.CharField(max_length=40, blank=True)
    meets_secretary = models.CharField(max_length=40, blank=True)
    social_secretary = models.CharField(max_length=40, blank=True)
    training_secretary = models.CharField(max_length=40, blank=True)
    webmaster = models.CharField(max_length=40, blank=True)
    librarian = models.CharField(max_length=40, blank=True)
    lamp_post = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return str(self.year)
