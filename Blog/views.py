from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import *
from datetime import datetime
from django.shortcuts import get_object_or_404, Http404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from django.forms.widgets import CheckboxSelectMultiple

class ModelFormWidgetMixin(object):
    ## Allow easy use of widgets in views
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)

class Blog(ListView):
    model = Post
    template_name = 'Meets/Blog.html'
    paginate_by = 5
    context_obect_name = 'post_list'
    queryset = Post.objects.all().order_by('-published_date')

@method_decorator(permission_required('Blog.add_post'), name='dispatch')
class BlogAdd(CreateView):
    model = Post
    template_name = 'Blog/PostForm.html'
    success_url = reverse_lazy('Blog')
    form_class =  modelform_factory(
        Post,
        fields = ['title', 'text', 'category', 'images'],
        widgets={"images": CheckboxSelectMultiple }
        )
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(permission_required('Blog.change_post'), name='dispatch')
class BlogEdit(UpdateView):
    model = Post
    template_name = 'Blog/PostForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('Blog')
    form_class =  modelform_factory(
        Post,
        fields = ['title', 'text', 'category', 'images'],
        widgets={"images": CheckboxSelectMultiple }
        )

@method_decorator(permission_required('Blog.delete_post'), name='dispatch')
class BlogDelete(DeleteView):
    model = Post
    template_name = 'Blog/PostForm.html'
    success_url = reverse_lazy('Blog')

@method_decorator(permission_required('Blog.add_image'), name='dispatch')
class ImageAdd(CreateView):
    model = Image
    template_name = 'Blog/ImageForm.html'
    fields = ['image', 'name']
    success_url = reverse_lazy('Blog')
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(permission_required('Blog.change_image'), name='dispatch')
class ImageEdit(UpdateView):
    model = Image
    template_name = 'Blog/ImageForm.html'
    fields = ['image', 'name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('Blog')

@method_decorator(permission_required('Blog.delete_image'), name='dispatch')
class ImageDelete(DeleteView):
    model = Image
    template_name = 'Blog/ImageForm.html'
    success_url = reverse_lazy('Blog')
