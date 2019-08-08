from django.shortcuts import render

def index(request):
    return render(request, 'StaticPages/index.html')
