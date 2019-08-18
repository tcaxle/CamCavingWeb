from UserPortal.models import CustomUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class Tag(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

def get_image_filename(instance, filename):
    date = instance.post.published_date
    slug = slugify(date)
    return "Blog/Images/%s-%s" % (slug, filename)

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def tag_display(self):
        return ', '.join([i.name for i in self.tag.all()])
    tag_display.short_description = 'Tag Display'

    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_filename, blank=True, null=True)

    def __str__(self):
        return str(self.images)
