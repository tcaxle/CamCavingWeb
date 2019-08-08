from django.shortcuts import render

# Homepage
def index(request):
    return render(request, 'StaticPages/index.html')

# About Section
def AboutMeetsFormatCost(request):
    return render(request, 'StaticPages/About/MeetsFormatCost.html')

def AboutTackleStore(request):
    return render(request, 'StaticPages/About/TackleStore.html')

def AboutLibrary(request):
    return render(request, 'StaticPages/About/Library.html')

def AboutConstitutionSafety(request):
    return render(request, 'StaticPages/About/ConstitutionSafety.html')

# Contact Section

# Gear Section

# Meets Section

# Get Involved Section
