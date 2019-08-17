from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4 as uuid

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
    committee = models.BooleanField(default=False, blank=False)
    email = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    user_key = models.CharField(max_length=32, default=uuid().hex)
    full_name = models.CharField(max_length=50, blank=False)
    college = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    tape_colour_1 = models.CharField(verbose_name='Gear Tape Colour 1', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_2 = models.CharField(verbose_name='Gear Tape Colour 2', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_3 = models.CharField(verbose_name='Gear Tape Colour 3', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_notes = models.CharField(verbose_name='Gear Tape Notes', max_length=50, blank=True)
    mailing_list = models.BooleanField(verbose_name='Subscribe to Mailing List?', blank=False, default=False)
    rank = models.ManyToManyField(Rank, verbose_name='Club Position')
    status = models.CharField(verbose_name='Status', max_length=20, choices=STATUS_CHOICES, blank=False, default='Inactive')

    def rank_display(self):
        return ', '.join([i.name for i in self.rank.all()])
    rank_display.short_description = 'Rank Display'

    def __str__(self):
        return self.username

class LegacyUser(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    college = models.CharField(max_length=50, blank=True)
    tape_colour_1 = models.CharField(verbose_name='Gear Tape Colour 1', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_2 = models.CharField(verbose_name='Gear Tape Colour 2', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_3 = models.CharField(verbose_name='Gear Tape Colour 3', max_length=6, choices=COLOR_CHOICES, default='', blank=True)
    tape_colour_notes = models.CharField(verbose_name='Gear Tape Notes', max_length=50, blank=True)
    rank = models.ManyToManyField(Rank, verbose_name='Club Position')
    status = models.CharField(verbose_name='Status', max_length=20, choices=STATUS_CHOICES, blank=False, default='Inactive')

    def rank_display(self):
        return ', '.join([i.name for i in self.rank.all()])

    def __str__(self):
        return self.full_name

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
