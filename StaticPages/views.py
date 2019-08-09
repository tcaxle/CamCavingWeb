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
def ContactCommittee(request):
    return render(request, 'StaticPages/Contact/Committee.html')
def ContactMailingList(request):
    return render(request, 'StaticPages/Contact/MailingList.html')

# Gear Section
def GearClub(request):
    return render(request, 'StaticPages/Gear/Club.html')
def GearPersonal(request):
    return render(request, 'StaticPages/Gear/Personal.html')

# Meets Section
def MeetsCalendar(request):
    return render(request, 'StaticPages/Meets/Calendar.html')
def MeetsBlog(request):
    return render(request, 'StaticPages/Meets/Blog.html')
def MeetsPub(request):
    return render(request, 'StaticPages/Meets/Pub.html')
def MeetsSocial(request):
    return render(request, 'StaticPages/Meets/Social.html')
def MeetsTraining(request):
    return render(request, 'StaticPages/Meets/Training.html')

# Get Involved Section
def GetInvolvedFreshers(request):
    return render(request, 'StaticPages/GetInvolved/Freshers.html')
def GetInvolvedHowToJoin(request):
    return render(request, 'StaticPages/GetInvolved/HowToJoin.html')
