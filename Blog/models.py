from UserPortal.models import CustomUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

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

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=POST_CATEGORIES, default='Caving', blank=False)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_filename, blank=True, null=True)

    def __str__(self):
        return str(self.images)
