from django.shortcuts import render
from UserPortal.models import CustomUser

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
def AboutTripsAbroad(request):
    return render(request, 'About/TripsAbroad.html')
def AboutBureaucracy(request):
    return render(request, 'About/Bureaucracy.html')

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
def MeetsDinners(request):
    return render(request, 'Meets/Dinners.html')

# Gear
def GearFirstAid(request):
    return render(request, 'Gear/FirstAid.html')
def GearHire(request):
    return render(request, 'Gear/Hire.html')
def GearInventory(request):
    return render(request, 'Gear/Inventory.html')
def GearTape(request):
    user_list = CustomUser.objects.all()
    context = {'user_list': user_list}
    return render(request, 'Gear/Tape.html', context)

# Get Involved
def GetInvolvedHowToJoin(request):
    return render(request, 'GetInvolved/HowToJoin.html')

# Library
def LibraryBooks(request):
    return render(request, 'Library/Books.html')
def LibraryMissingBooks(request):
    return render(request, 'Library/MissingBooks.html')

# Misc
def MiscCommitteeFunctions(request):
    return render(request, 'Misc/CommitteeFunctions.html')
def MiscNCAGuidelines(request):
    return render(request, 'Misc/NCAGuidelines.html')
def MiscExCS(request):
    return render(request, 'Misc/ExCS.html')
def MiscNoviceChecklist(request):
    return render(request, 'Misc/NoviceChecklist.html')
def MiscLeaderChecklist(request):
    return render(request, 'Misc/LeaderChecklist.html')

# Ardeche
def ArdecheAgas(request):
    return render(request, 'Ardeche/Agas.html')
def ArdecheBarry(request):
    return render(request, 'Ardeche/Barry.html')
def ArdecheBunis(request):
    return render(request, 'Ardeche/Bunis.html')
def ArdecheCadet(request):
    return render(request, 'Ardeche/Cadet.html')
def ArdecheCamilie(request):
    return render(request, 'Ardeche/Camilie.html')
def ArdecheCentura(request):
    return render(request, 'Ardeche/Centura.html')
def ArdecheChampclos(request):
    return render(request, 'Ardeche/Champclos.html')
def ArdecheChataigniers(request):
    return render(request, 'Ardeche/Chataigniers.html')
def ArdecheChazot(request):
    return render(request, 'Ardeche/Chazot.html')
def ArdecheChenivesse(request):
    return render(request, 'Ardeche/Chenivesse.html')
def ArdecheChevre(request):
    return render(request, 'Ardeche/Chevre.html')
def ArdecheCombeRajeau(request):
    return render(request, 'Ardeche/CombeRajeau.html')
def ArdecheCotepatiere(request):
    return render(request, 'Ardeche/Cotepatiere.html')
def ArdecheCourtinen(request):
    return render(request, 'Ardeche/Courtinen.html')
def ArdecheDerocs(request):
    return render(request, 'Ardeche/Derocs.html')
def ArdecheDragonniere(request):
    return render(request, 'Ardeche/Dragonniere.html')
def ArdecheFauxMarzal(request):
    return render(request, 'Ardeche/FauxMarzal.html')
def ArdecheFontlongue(request):
    return render(request, 'Ardeche/Fontlongue.html')
def ArdecheFoussoubie(request):
    return render(request, 'Ardeche/Foussoubie.html')
def ArdecheGauthier(request):
    return render(request, 'Ardeche/Gauthier.html')
def ArdecheGrandBadingue(request):
    return render(request, 'Ardeche/GrandBadingue.html')
def ArdecheGregoire(request):
    return render(request, 'Ardeche/Gregoire.html')
def ArdecheMarteau(request):
    return render(request, 'Ardeche/Marteau.html')
def ArdecheNeufGorges(request):
    return render(request, 'Ardeche/NeufGorges.html')
def ArdecheNoel(request):
    return render(request, 'Ardeche/Noel.html')
def ArdechePebres(request):
    return render(request, 'Ardeche/Pebres.html')
def ArdechePeyrejal(request):
    return render(request, 'Ardeche/Peyrejal.html')
def ArdecheReynaud(request):
    return render(request, 'Ardeche/Reynaud.html')
def ArdecheRichard(request):
    return render(request, 'Ardeche/Richard.html')
def ArdecheRochas(request):
    return render(request, 'Ardeche/Rochas.html')
def ArdecheRosa(request):
    return render(request, 'Ardeche/Rosa.html')
def ArdecheRouveyrette(request):
    return render(request, 'Ardeche/Rouveyrette.html')
def ArdecheStMarcel(request):
    return render(request, 'Ardeche/StMarcel.html')
def ArdecheVarade(request):
    return render(request, 'Ardeche/Varade.html')
def ArdecheVigneClose(request):
    return render(request, 'Ardeche/VigneClose.html')
