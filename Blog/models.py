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

class Image(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_filename, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name+' ('+str(self.image)+')'

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=POST_CATEGORIES, blank=False)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField(Image, blank=True, null=True)

    def __str__(self):
        return self.title
