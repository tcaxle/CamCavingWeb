from django.shortcuts import render

# Homepage
def Home(request):
    return render(request, 'Home.html')

# About Section
def AboutMeetsFormatCost(request):
    return render(request, 'About/MeetsFormatCost.html')
def AboutTackleStore(request):
    return render(request, 'About/TackleStore.html')
def AboutLibrary(request):
    return render(request, 'About/Library.html')
def AboutConstitutionSafety(request):
    return render(request, 'About/ConstitutionSafety.html')
def AboutExpo(request):
    return render(request, 'About/Expo.html')
def AboutBureaucracy(request):
    return render(request, 'About/Bureaucracy.html')
def AboutArchive(request):
    return render(request, 'About/Archive.html')

# Contact Section
def ContactCommittee(request):
    return render(request, 'Contact/Committee.html')
def ContactMailingList(request):
    return render(request, 'Contact/MailingList.html')

# Meets Section
def MeetsCalendar(request):
    return render(request, 'Meets/Calendar.html')
def MeetsBlog(request):
    return render(request, 'Meets/Blog.html')
def MeetsPub(request):
    return render(request, 'Meets/Pub.html')
def MeetsSocial(request):
    return render(request, 'Meets/Social.html')
def MeetsTraining(request):
    return render(request, 'Meets/Training.html')

# Get Involved Section
def GetInvolvedHowToJoin(request):
    return render(request, 'GetInvolved/HowToJoin.html')
