from UserPortal.models import CustomUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from django.contrib.postgres.fields import JSONField

from CamCavingWeb.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT_DIR as STATIC_ROOT, SSH_PATH, REMOTE_MEDIA_URL

import os

def get_image_filename(instance, filename):
    date = instance.post.published_date
    slug = slugify(date)
    return "Blog/Images/%s-%s" % (slug, filename)

POST_CATEGORIES = (
    ('News', 'News'),
    ('Caving', 'Caving'),
    ('Training', 'Training'),
    ('Social', 'Social'),
)

class Image(models.Model):
    album = models.ForeignKey("Album", on_delete=models.CASCADE, null=False)
    image_filename = models.CharField(max_length=512) # relative to Album on cucc.survex.com/media
    thumb_filename = models.CharField(max_length=512) # relative to Album directory
    photographer = models.CharField(max_length=100, blank=True, default="")
    timestamp = models.DateTimeField(default=None, null=True, blank=True)
    description = models.TextField(blank=True, default="")
    metadata = JSONField(blank=True)

    def get_thumb_path(self):
        return os.path.join(self.album.get_path(), self.thumb_filename)

    def get_thumb_url(self):
        return os.path.join(self.album.get_url(), self.thumb_filename)

    def get_url(self):
        return os.path.join(REMOTE_MEDIA_URL, self.album.directory, self.image_filename)


class Post(models.Model):
    posted_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    author = models.CharField(max_length=100, blank=False, default="")
    category = models.CharField(max_length=10, choices=POST_CATEGORIES, blank=False)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    # images = models.ManyToManyField(Image, blank=True, null=True)

    def __str__(self):
        return str(self.title) + " by " + self.author

class Album(models.Model):
    title = models.CharField(max_length=200, blank=False)
    date = models.DateField(default=timezone.now, blank=False)
    directory = models.CharField(max_length=512, blank=False, unique=True)
    parent = models.ForeignKey("Album", on_delete=models.CASCADE, null=True, blank=True)
    cover_image = models.CharField(max_length=512, null=True, blank=True) # Non-compulsory cover image for the album

    def __str__(self):
        return str(self.title) + " [" + str(self.date) + "]"

    def get_path(self):
        return os.path.join(MEDIA_ROOT, 'Albums', self.directory)

    def get_url(self):
        return os.path.join(MEDIA_URL, "Albums", self.directory)

    class Meta:
        ordering = ['-date']

class Trip(models.Model):
    name = models.CharField(max_length=200, blank=True) # could be NCHECC 2020 or New Year's Party
    location = models.CharField(max_length=200, blank=False) # would be South Wales
    hut = models.CharField(max_length=200, blank=False) # SWCC
    date = models.DateField(default=timezone.now)
    days = models.IntegerField(default=2)
    # leader = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='leader', null=True, blank=True)
    leader = models.CharField(max_length=200)
    # attendees = models.ManyToManyField(CustomUser, related_name='attendees')
    attendees = models.CharField(max_length=4096, default="", blank=True)
    # attendees_wo_account = models.TextField(blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    posts = models.ManyToManyField(Post, blank=True)
    is_expo = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=True)
    is_freshers_trip = models.BooleanField(default=False)
    is_missing_info = models.BooleanField(default=False)
    comments = models.TextField(default="", blank=True)

    def __str__(self):
        s = str(self.name)
        if str(self.name) != "":
            s += " in "

        s += str(self.location) + " (" + str(self.hut) + ") [" + str(self.date) + "]"

        if not self.is_confirmed:
            s += " [Unconfirmed Trip]"

        return s

    class Meta:
        ordering = ['-date']