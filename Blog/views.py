from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageForm, PostForm
from .models import *
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

def Blog(request):
    post_list = Post.objects.all().order_by('-published_date')
    image_list = Image.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'Meets/Blog.html', { 'posts': posts, 'image_list': image_list })

@login_required(login_url='/Portal/login/')
def BlogPost(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=10)
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.author = request.user
            post_form.save()
            for form in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Image(post=post_form, images=image)
                    photo.save()
            messages.success(request,"Success")
            return redirect("/Blog")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'Blog/Post.html', {'postForm': postForm, 'formset': formset})

@login_required(login_url='/Portal/login/')
def BlogEdit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/Blog', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'Blog/Edit.html', {'form': form})

@login_required(login_url='/Portal/login/')
def BlogDelete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/Blog')
