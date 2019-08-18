from django import forms
from .models import *

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('image', )
