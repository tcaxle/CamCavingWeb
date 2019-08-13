from django.shortcuts import render

# Homepage
def Home(request):
    return render(request, 'Home.html')

# About
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

# Contact
def ContactCommittee(request):
    return render(request, 'Contact/Committee.html')
def ContactMailingList(request):
    return render(request, 'Contact/MailingList.html')

# Meets
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

# Get Involved
def GetInvolvedHowToJoin(request):
    return render(request, 'GetInvolved/HowToJoin.html')

# Library
def LibraryBooks(request):
    return render(request, 'Library/Books.html')
def LibraryMissingBooks(request):
    return render(request, 'Library/MissingBooks.html')
