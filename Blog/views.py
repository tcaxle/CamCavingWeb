from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import *
from datetime import datetime
from django.shortcuts import get_object_or_404, Http404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.forms.models import modelform_factory
from django.forms.widgets import CheckboxSelectMultiple
from django import http
import os
from CamCavingWeb.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT_DIR as STATIC_ROOT, SSH_PATH, REMOTE_MEDIA_URL
from CamCavingWeb.views import generate_multialbum_view, single_album_view

from collections import OrderedDict

from scripts.thumbs import thumbify

import pysftp
from shutil import copyfile

import PIL.Image
import PIL.ExifTags

from datetime import datetime

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None   

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

class BlogByAuthor(ListView):
    model = Post
    template_name = 'Meets/Blog.html'
    paginate_by = 5
    context_obect_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all().order_by('-published_date').filter(author=self.kwargs['author'])
        # return Message.objects.filter(lab__acronym=self.kwargs['lab'])

    def get_context_data(self, **kwargs):
        context = super(BlogByAuthor, self).get_context_data(**kwargs)
        # Add in the publisher
        context['by_author'] = True
        return context


@method_decorator(permission_required('Blog.add_post'), name='dispatch')
class BlogAdd(CreateView):
    model = Post
    template_name = 'Blog/PostForm.html'
    success_url = reverse_lazy('Blog')
    form_class =  modelform_factory(
        Post,
        fields = ['title', 'text', 'category', 'author', 'date'],
        # fields = ['title', 'text', 'category', 'images', 'author'],
        widgets={"images": CheckboxSelectMultiple }
        )
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

@method_decorator(permission_required('Blog.change_post'), name='dispatch')
class BlogEdit(UpdateView):
    model = Post
    template_name = 'Blog/PostForm.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('Blog')
    form_class =  modelform_factory(
        Post,
        fields = ['title', 'text', 'category', 'author', 'date'],
        # fields = ['title', 'text', 'category', 'images', 'author'],
        # widgets={"images": CheckboxSelectMultiple }
        )

@method_decorator(permission_required('Blog.delete_post'), name='dispatch')
class BlogDelete(DeleteView):
    model = Post
    template_name = 'Blog/PostForm.html'
    success_url = reverse_lazy('Blog')

# @method_decorator(permission_required('Blog.add_image'), name='dispatch')
# class ImageAdd(CreateView):
#     model = Image
#     template_name = 'Blog/ImageForm.html'
#     fields = ['image', 'name']
#     success_url = reverse_lazy('Blog')
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)

@method_decorator(permission_required('Blog.change_image'), name='dispatch')
class ImageEdit(UpdateView):
    model = Image
    template_name = 'Blog/ImageEdit.html'
    fields = ['photographer', 'timestamp', 'description', 'metadata']

    def get_success_url(self, **kwargs):         
        return reverse('ImageView', args=(self.object.pk,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thumb_url'] = self.object.get_thumb_url()
        context['image_url'] = self.object.get_url()
        return context

class ImageView(DetailView):
    template_name = 'Blog/ImageView.html'

    model = Image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["image"] = self.object
        context["album"] = self.object.album

        return context

def AlbumList(request):
    context = {}
    context['albums'] = generate_multialbum_view()

    return render(request, "Blog/AlbumList.html", context)

def recrusive_child_album_list_builder(album):
    child_albums = list(Album.objects.filter(parent__id=album.pk))

    for child_album in child_albums:
        child_albums += recrusive_child_album_list_builder(child_album)

    return child_albums

permission_required('Blog.edit_album')
def UpdateAlbumImages(request, pk):

    import shutil

    album = get_object_or_404(Album, pk=pk)
    directory = album.directory

    albums_dir = os.path.join(MEDIA_ROOT, 'Albums') # local albums path
    local_dir = os.path.join(MEDIA_ROOT, 'Albums', directory) # local album path
    vid_thumb = os.path.join(STATIC_ROOT, "images/vid_thumb.png")

    print("local_dir", local_dir)
    print("directory_name", directory)

    conn = pysftp.Connection("cucc.survex.com", username="cuccmedia", private_key=os.path.join(SSH_PATH, "cuccmedia"), cnopts=cnopts)

    if not conn.isdir(os.path.join("media", directory)):
        return "Not a directory"

    # print("Directory listing")

    remote_dirs = []
    remote_files = []
    remote_others = []

    conn.walktree(os.path.join("media", directory), remote_files.append, remote_dirs.append, remote_others.append, recurse=False)

    remote_files = [file.replace("media/", "") for file in remote_files]
    remote_dirs = [file.replace("media/", "") for file in remote_dirs]
    remote_others = [file.replace("media/", "") for file in remote_others]

    # print("++++++++++++++++++++++=")

    # print("Other files", remote_files)
    print("Other dirs", remote_dirs)
    # print("++++++++++++++++++++++=")

    local_dirs = []
    local_files = []

    for root, dirs, files in os.walk(local_dir):
        root = root.replace(albums_dir+"/", "")
        # print("root", root)
        files = [os.path.join(root, "".join(file.split("_thumb"))) for file in files] # removes "_thumb" part of file name to make the equivalent
        dirs = [os.path.join(root, file) for file in dirs]
        # print(root, dirs, files)
        local_files += files
        local_dirs += dirs

        break # stops the function after one iteration --> stops recursion

    # print("local files", local_files)
    print("local dirs", local_dirs)

    # print("++++++++++++++++++++++=")


    local_only_files = set(local_files).difference(remote_files)
    remote_only_files = set(remote_files).difference(local_files)

    local_only_dirs = set(local_dirs).difference(remote_dirs)
    remote_only_dirs = set(remote_dirs).difference(local_dirs)

    print("local only files", local_only_files)
    print("remote only files", remote_only_files)

    print("local only dirs", local_only_dirs)
    print("remote only dirs", remote_only_dirs)

    child_albums = recrusive_child_album_list_builder(album)
    child_albums = [(album, album.directory) for album in child_albums]

    print("child_albums", child_albums)

    for file in local_only_files:

        basename = ".".join(file.split(".")[0:-1])
        extenstion = file.split(".")[-1]

        os.remove(os.path.join(albums_dir, "{}_thumb.{}".format(basename, extenstion)))
        print("removing", os.path.join(albums_dir, "{}_thumb.{}".format(basename, extenstion)))

    for dir in local_only_dirs:
        # os.rmdir(os.path.join(albums_dir, dir))
        shutil.rmtree(os.path.join(albums_dir, dir))
        # remove appropriate albums

        for child_album in child_albums:
            if child_album[1] == dir:
                print("found", dir)
                child_album[0].delete()
                print("removing child album")

        print("removing", os.path.join(albums_dir, dir))

    for dir in remote_only_dirs:
        os.makedirs(os.path.join(albums_dir, dir))

        found = False

        for child_album in child_albums:
            if child_album[1] == dir:
                print("found, skipping album creation", dir)
                found=True

        if not found:
            sub_album = Album(title=dir.split("/")[-1], date=album.date, directory=dir, parent=album, cover_image=None)
            sub_album.save()
            print("creating", os.path.join(albums_dir, dir))
        # add appropriate albums

    for file in remote_only_files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(os.path.join("media", file), os.path.join(albums_dir, file))
            conn.get(os.path.join("media", file), localpath=os.path.join(albums_dir, file))
            thumbify(os.path.join(albums_dir, file))
            os.remove(os.path.join(albums_dir, file))
        elif file.lower().endswith(('.mov', '.mp4', '.avi', '.mkv')):
            print(os.path.join("media", file), os.path.join(albums_dir, file))
            print(vid_thumb, os.path.join(albums_dir, file))
            basename = ".".join(file.split(".")[0:-1])
            extenstion = file.split(".")[-1]
            copyfile(vid_thumb, os.path.join(albums_dir, "{}_thumb.{}".format(basename, extenstion)))


    return redirect(reverse('Album')+"/"+str(album.pk))

permission_required('Blog.edit_album')
def UpdateDBImages(request, pk):

    import shutil
    import regex

    album = get_object_or_404(Album, pk=pk)
    directory = album.directory

    albums_dir = os.path.join(MEDIA_ROOT, 'Albums') # local albums path
    local_dir = os.path.join(MEDIA_ROOT, 'Albums', directory) # local album path
    vid_thumb = os.path.join(STATIC_ROOT, "images/vid_thumb.png")

    fs_images = []

    for root, dirs, files in os.walk(local_dir):
        root = root.replace(albums_dir+"/", "")
        fs_images += files

        break # stops recursion

    db_images = [image.thumb_filename for image in Image.objects.filter(album=album)]

    problem_fileds = ["UserComment", "MakerNote", "GPSInfo", "ImageUniqueID"]

    print("FS", fs_images)
    print("DB", db_images)

    fs_only_images = set(fs_images).difference(db_images)
    db_only_images = set(db_images).difference(fs_images)

    print("FS only", fs_only_images)
    print("DB only", db_only_images)

    for image in fs_only_images:
        image_path = os.path.join(albums_dir, album.directory, image)
        # print(image_path)

        img = PIL.Image.open(image_path)
        exif_data = img._getexif()

        # print(exif_data)

        exif = {}
        timestamp = None

        if exif_data is not None:
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }

            # print("+++")

            for pf in problem_fileds:
                if pf in exif:
                    del exif[pf]

            for k,v in exif.items():
                # print(k, v, type(v))
                if str(type(v)) == "<class 'bytes'>" :
                    # print("convert------")
                    exif[k] = v.hex() # converts all bytes to their hex repr
                # print(k, v)

            # print("====")

            # for k,v in exif.items():
                # print(k, v, type(v))

            # print(exif)

            if "DateTimeOriginal" in exif:
                timestamp = exif["DateTimeOriginal"]
            elif "DateTime" in exif:
                timestamp = exif["DateTime"]
            elif "DateTimeDigitized" in exif:
                timestamp = exif["DateTimeDigitized"]
            else:
                timestamp=None

            if timestamp is not None:
                year = timestamp[0:4]
                month = timestamp[5:7]
                day = timestamp[8:10]
                hour = timestamp[11:13]
                minutes = timestamp[14:16]
                seconds = timestamp[17:19]
    
                timestamp = "{}-{}-{} {}:{}:{}".format(year, month, day, hour, minutes, seconds)
        else:
            # print("fiename", image)
            unformatted = regex.search(r"([0-9]{4})([0-9]{2})([0-9]{2})_([0-9]{2})([0-9]{2})([0-9]{2})_", image, regex.M|regex.U)
            if unformatted is not None:
                groups = unformatted.groups()
                # print(groups)
                timestamp = datetime(int(groups[0]), int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4]), int(groups[5]))

        # print(image)
        # print(timestamp)

        try:
            Image(album=album, image_filename="".join(image.split("_thumb")), thumb_filename=image, metadata=exif, timestamp=timestamp).save()
        except Exception as e:
            print("Failed to generate database entry for image at `{}` with thumbnail `{}`.".format("".join(image.split("_thumb")), image))
            print(e)


    return redirect(reverse('Album')+"/"+str(album.pk))


@method_decorator(permission_required('Blog.add_album'), name='dispatch')
class AlbumAdd(CreateView):
    model = Album
    template_name = 'Blog/AlbumAdd.html'
    success_url = reverse_lazy('Album')
    form_class =  modelform_factory(
        Album,
        fields = ['title', 'date', 'directory', 'cover_image']
        )
    def form_valid(self, form):
        form.instance.directory = form.instance.directory.replace("/", "")
        directory = form.instance.directory
        albums_dir = os.path.join(MEDIA_ROOT, 'Albums') # local albums path
        local_dir = os.path.join(MEDIA_ROOT, 'Albums', directory) # local album path
        vid_thumb = os.path.join(STATIC_ROOT, "images/vid_thumb.png")

        print("validating form")
        # 1. Connect to Wokkie's Server to check if directory exists
        # 2. Create same local directory and mirror directory structure
        # 3. If yes, download images, generate thumbnails, for videos, create placeholder thumbnail


        conn = pysftp.Connection("cucc.survex.com", username="cuccmedia", private_key=os.path.join(SSH_PATH, "cuccmedia"), cnopts=cnopts)

        if not conn.isdir(os.path.join("media", directory)):
            return "Not a directory"

        print("Directory listing")

        dirs = []
        files = []
        others = []

        conn.walktree(os.path.join("media", directory), files.append, dirs.append, others.append, recurse=False)

        files = [file.replace("media/", "") for file in files]
        dirs = [file.replace("media/", "") for file in dirs]
        others = [file.replace("media/", "") for file in others]

        print("Files", files)
        print("Dirs", dirs)
        print("Others", others)

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

            for d in dirs:
                os.makedirs(os.path.join(albums_dir, d))

        else:
            print("Path already exists")
            # return "Path already exists" # CAN'T RETURN A STRING FROM THIS METHOD
            return super().form_invalid(form)

        # Create album

        self.object = form.save(commit=False)
        self.object.parent = None
        if self.object.cover_image is not None:
            basename = ".".join(self.object.cover_image.split(".")[0:-1])
            extenstion = self.object.cover_image.split(".")[-1]
            self.object.cover_image = "{}_thumb.{}".format(basename, extenstion)
        self.object.save()

        for directory in dirs:
            # directory = '2020-01-02-05 Scottland Hillwalking/Day 1 - Ben Cruachan'
            print("Creating sub-album for", directory)
            directory_name = directory.split("/")[-1]
            print("title", directory_name, "date", self.object.date, "directory", directory, "parent", self.object)
            sub_album = Album(title=directory_name, date=self.object.date, directory=directory, parent=self.object, cover_image=None)
            sub_album.save()

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(os.path.join("media", file), os.path.join(albums_dir, file))
                conn.get(os.path.join("media", file), localpath=os.path.join(albums_dir, file))
                thumbify(os.path.join(albums_dir, file))
                os.remove(os.path.join(albums_dir, file))
            elif file.lower().endswith(('.mov', '.mp4', '.avi', '.mkv')):
                print(os.path.join("media", file), os.path.join(albums_dir, file))
                # conn.get(os.path.join("media", file), localpath=os.path.join(albums_dir, file))
                print(vid_thumb, os.path.join(albums_dir, file))
                basename = ".".join(file.split(".")[0:-1])
                extenstion = file.split(".")[-1]
                copyfile(vid_thumb, os.path.join(albums_dir, "{}_thumb.{}".format(basename, extenstion)))
                # os.remove(os.path.join(albums_dir, file))
                # pass
            

        conn.close()

        # return super().form_valid(form)

        return http.HttpResponseRedirect(self.get_success_url())

@method_decorator(permission_required('Blog.edit_album'), name='dispatch')
class AlbumCoverUpdate(DetailView):
    template_name = 'Blog/AlbumCoverEdit.html'

    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        album_url = os.path.join(MEDIA_URL, 'Albums', self.object.directory)
        if self.object.cover_image is not None:
            context["cover"] = os.path.join(album_url, self.object.cover_image)
        else:
            context["cover"] = ""

        child_albums = Album.objects.filter(parent__id=self.object.pk).order_by('date') # not going deeper than 1 level

        # image_list = (image_thumb_url, file_name_relative_to_root_album)

        thumb_root_url = os.path.join(MEDIA_URL, "Albums", self.object.directory)
        album_dir = os.path.join(MEDIA_ROOT, 'Albums', self.object.directory)

        image_list = [(os.path.join(thumb_root_url, file), file) for file in sorted(os.listdir(album_dir)) if (file.lower().endswith(('.png', '.jpg', '.jpeg')) and "_thumb." in file)]

        for child_album in child_albums:
            print(child_album.title)
            for file in sorted(os.listdir(os.path.join(MEDIA_ROOT, 'Albums', child_album.directory))):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')) and "_thumb." in file:
                    image_list.append((os.path.join(MEDIA_URL, "Albums", child_album.directory, file), os.path.join(child_album.directory, file).replace(self.object.directory + "/", "")))

        context["images"] = image_list
        context["pk"] = self.object.pk

        return context

@permission_required('Blog.edit_album')
def AlbumCoverUpdateSet(request, pk):
    if request.method == 'POST':
        album = get_object_or_404(Album, pk=pk)
        image_name = request.POST.get('cover')
        print("image name", image_name)
        album.cover_image = image_name
        album.save()

        if album.parent is None:
            return redirect(reverse('Album'))
        else:
            return redirect(reverse('Album')+"/"+str(album.parent.pk))
            
    return redirect(reverse('Album'))


def AlbumView(request, pk):
    album = get_object_or_404(Album, pk=pk)
    dir = os.path.join(MEDIA_ROOT, 'Albums', album.directory)
    vid_thumb = os.path.join(STATIC_URL, "images/vid_thumb.png")
    dir_thumb = os.path.join(STATIC_URL, "images/dir_thumb.png")
    thumb_root_url = os.path.join(MEDIA_URL, "Albums", album.directory)
    # image_root_url = os.path.join("http://cucc.survex.com/media/", album.directory)
    image_root_url = os.path.join(REMOTE_MEDIA_URL, album.directory)

    # print([x[0] for x in os.walk(dir)])

    # display_list = [(os.path.join(album_root_url, file), os.path.join(album_root_url, file)) for file in os.listdir(dir) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.mov', '.mp4', '.avi', '.mkv'))]
    # image_list = [(http://image/url.xyz, http://thumbnail/url.xyz, image object from DB), ...]

    album_list = []

    # child_albums = album.parent_set.all()
    child_albums = Album.objects.filter(parent__id=pk).order_by('date')

    for child_album in child_albums:
        album_list.append(single_album_view(child_album))

    db_images = {image.image_filename: image for image in Image.objects.filter(album=album)}

    # print(db_images)
    
    image_list = [(os.path.join(image_root_url, "".join(file.split("_thumb"))), os.path.join(thumb_root_url, file)) for file in sorted(os.listdir(dir)) if (file.lower().endswith(('.png', '.jpg', '.jpeg')) and "_thumb." in file) or file.lower().endswith(('.mov', '.mp4', '.avi', '.mkv'))]
    for i in range(len(image_list)):
        filename = image_list[i][0].split("/")[-1]
        print(filename)
        if image_list[i][0].lower().endswith(('.mov', '.mp4', '.avi', '.mkv')):
            if filename in db_images:
                image_list[i] = (image_list[i][0], vid_thumb, db_images[filename])
            else:
                image_list[i] = (image_list[i][0], vid_thumb, False)
        else:
            if filename in db_images:
                image_list[i] = (image_list[i][0], image_list[i][1], db_images[filename])
            else:
                image_list[i] = (image_list[i][0], image_list[i][1], False)
        # image_list[i] = (image_list[i][0], image_list[i][1])


    context = {}
    context['images'] = image_list
    context['child_albums'] = album_list
    context['album'] = album

    # print(image_list)

    return render(request, 'Blog/AlbumView.html', context)

@method_decorator(permission_required('Blog.add_trip'), name='dispatch')
class TripAdd(CreateView):
    model = Trip
    template_name = 'Blog/TripAdd.html'
    success_url = reverse_lazy('Trip')
    form_class =  modelform_factory(
        Trip,
        fields = ['name', 'location', 'hut', 'date', 'days', 'leader', 'attendees', 'album', 'posts', 'is_expo', 'is_confirmed', 'is_missing_info', 'comments']
        )
    def form_valid(self, form):
        # return http.HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

def make_trip_list(trips):
    by_year = OrderedDict()

    for trip in trips:
        year = trip.date.year
        print(year)
        if not year in by_year:
            by_year[year] = []
        by_year[year].append(trip)

    return by_year

def TripList(request):
    context = {}
    context['trips'] = Trip.objects.order_by('-date')

    context['by_year'] = make_trip_list(context['trips'])

    years = set()
    for trip in Trip.objects.all():
        years.add(trip.date.year)
    years = sorted([int(k) for k in years], reverse=True)

    context["years"] = years
    context["title"] = "All Years"

    return render(request, "Blog/TripList.html", context)

def TripListByYear(request, year):
    context = {}
    context['trips'] = Trip.objects.order_by('-date').filter(date__year=year)

    context['by_year'] = make_trip_list(context['trips'])

    years = set()
    later_years = set()

    for trip in Trip.objects.all():
        years.add(trip.date.year)
        if int(trip.date.year) > year:
            later_years.add(trip.date.year)

    years = sorted([int(k) for k in years], reverse=True)
    later_years = sorted([int(k) for k in later_years], reverse=True)

    context["year"] = year
    context["years"] = years
    context["later_years"] = later_years
    context["title"] = str(year)

    return render(request, "Blog/TripList.html", context)

def TripListByRange(request, year_start, year_end):
    context = {}
    context['trips'] = Trip.objects.order_by('-date').filter(date__year__gte=year_start).filter(date__year__lte=year_end)

    context['by_year'] = make_trip_list(context['trips'])

    years = set()

    for trip in Trip.objects.all():
        years.add(trip.date.year)

    years = sorted([int(k) for k in years], reverse=True)

    context["years"] = years
    context["year_start"] = year_start
    context["year_end"] = year_end
    context["title"] = str(year_start) + " - " + str(year_end)

    return render(request, "Blog/TripList.html", context)

def make_stats(trips, reports):

    trip_attending = {}
    trip_leading = {}
    report_writing = {}

    trip_attending_weighted = {} # take length into account
    trip_leading_weighted = {}


    for trip in trips:
        attendees = trip.attendees.split(", ")
        for attendee in attendees:
            if not attendee in trip_attending:
                trip_attending[attendee] = 0
            if not attendee in trip_attending_weighted:
                trip_attending_weighted[attendee] = 0

            trip_attending[attendee] += 1
            trip_attending_weighted[attendee] += trip.days

        if not trip.leader in trip_leading:
            trip_leading[trip.leader] = 0
        trip_leading[trip.leader] += 1
    
        if not trip.leader in trip_leading_weighted:
            trip_leading_weighted[trip.leader] = 0
        trip_leading_weighted[trip.leader] += trip.days


    for report in reports:
        if not report.author in report_writing:
            report_writing[report.author] = 0
        report_writing[report.author] += 1

    # print(trip_leading)

    return {
        "trip_attending_weighted": sorted([(k, v) for k, v in trip_attending_weighted.items()], key=lambda x: x[1], reverse=True),
        "trip_attending": sorted([(k, v) for k, v in trip_attending.items()], key=lambda x: x[1], reverse=True),
        "trip_leading_weighted": sorted([(k, v) for k, v in trip_leading_weighted.items()], key=lambda x: x[1], reverse=True),
        "trip_leading": sorted([(k, v) for k, v in trip_leading.items()], key=lambda x: x[1], reverse=True),
        "report_writing": sorted([(k, v) for k, v in report_writing.items()], key=lambda x: x[1], reverse=True),
    }

def TripStats(request): # show number of trips per person, number of times a person has lead a trip and number of reports written per person

    stats = make_stats(Trip.objects.all(), Post.objects.filter(category="Caving"))
    years = set()
    for trip in Trip.objects.all():
        years.add(trip.date.year)

    for post in Post.objects.all():
        years.add(post.date.year)

    years = sorted([int(k) for k in years], reverse=True)

    stats["years"] = years
    stats["title"] = "All Years"

    return render(request, "Blog/TripStats.html", stats)

def TripStatsByYear(request, year): # show number of trips per person, number of times a person has lead a trip and number of reports written per person

    stats = make_stats(Trip.objects.filter(date__year=year), Post.objects.filter(category="Caving").filter(date__year=year))
    years = set()

    later_years = set()

    for trip in Trip.objects.all():
        years.add(trip.date.year)
        if int(trip.date.year) > year:
            later_years.add(trip.date.year)

    for post in Post.objects.all():
        years.add(post.date.year)
        if int(post.date.year) > year:
            later_years.add(post.date.year)

    years = sorted([int(k) for k in years], reverse=True)
    later_years = sorted([int(k) for k in later_years], reverse=True)

    stats["year"] = year
    stats["years"] = years
    stats["later_years"] = later_years
    stats["title"] = str(year)


    return render(request, "Blog/TripStats.html", stats)

def TripStatsByRange(request, year_start, year_end): # show number of trips per person, number of times a person has lead a trip and number of reports written per person

    stats = make_stats(Trip.objects.filter(date__year__gte=year_start).filter(date__year__lte=year_end), Post.objects.filter(category="Caving").filter(date__year__gte=year_start).filter(date__year__lte=year_end))
    years = set()

    for trip in Trip.objects.all():
        years.add(trip.date.year)

    for post in Post.objects.all():
        years.add(post.date.year)
    years = sorted([int(k) for k in years], reverse=True)

    stats["years"] = years
    stats["year_start"] = year_start
    stats["year_end"] = year_end
    stats["title"] = str(year_start) + " - " + str(year_end)

    return render(request, "Blog/TripStats.html", stats)
