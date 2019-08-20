from django.shortcuts import render, redirect
from UserPortal.models import *
from Blog.models import *
from Gear.models import *
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

# Homepage
class Home(ListView):
    model = Post
    template_name = 'Home.html'
    paginate_by = 5
    context_obect_name = 'post_list'
    queryset = Post.objects.filter(category='News').order_by('-published_date')

# About
class AboutMeetsFormatCost(TemplateView):
    template_name = 'About/MeetsFormatCost.html'
class AboutTackleStore(TemplateView):
    template_name = 'About/TackleStore.html'
class AboutLibrary(TemplateView):
    template_name = 'About/Library.html'
class AboutConstitutionSafety(TemplateView):
    template_name = 'About/ConstitutionSafety.html'
class AboutExpo(TemplateView):
    template_name = 'About/Expo.html'
class AboutTripsAbroad(TemplateView):
    template_name = 'About/TripsAbroad.html'
class AboutBureaucracy(TemplateView):
    template_name = 'About/Bureaucracy.html'

# Contact
class ContactCommittee(ListView):
    model = Committee
    template_name = 'Contact/Committee.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = CustomUser.objects.all().order_by('full_name')
        context['rank_list'] = Rank.objects.all()
        context['committee_list'] = Committee.objects.all().order_by('-year')
        return context
class ContactMailingList(TemplateView):
    template_name = 'Contact/MailingList.html'

# Meets
class MeetsCalendar(TemplateView):
    template_name = 'Meets/Calendar.html'
class MeetsPub(TemplateView):
    template_name = 'Meets/Pub.html'
class MeetsSocial(ListView):
    model = Post
    template_name = 'Meets/Social.html'
    paginate_by = 5
    context_obect_name = 'post_list'
    queryset = Post.objects.filter(category='Social').order_by('-published_date')
class MeetsTraining(ListView):
    model = Post
    template_name = 'Meets/Training.html'
    paginate_by = 5
    context_obect_name = 'post_list'
    queryset = Post.objects.filter(category='Training').order_by('-published_date')
class MeetsCaving(ListView):
    model = Post
    template_name = 'Meets/Caving.html'
    paginate_by = 5
    context_obect_name = 'post_list'
    queryset = Post.objects.filter(category='Caving').order_by('-published_date')
class MeetsDinners(TemplateView):
    template_name = 'Meets/Dinners.html'

# Get Involved
class GetInvolvedHowToJoin(TemplateView):
    template_name = 'GetInvolved/HowToJoin.html'

# Library
class LibraryBooks(TemplateView):
    template_name = 'Library/Books.html'
class LibraryMissingBooks(TemplateView):
    template_name = 'Library/MissingBooks.html'

# Misc
class MiscCommitteeFunctions(TemplateView):
    template_name = 'Misc/CommitteeFunctions.html'
class MiscNCAGuidelines(TemplateView):
    template_name = 'Misc/NCAGuidelines.html'
class MiscExCS(TemplateView):
    template_name = 'Misc/ExCS.html'
class MiscNoviceChecklist(TemplateView):
    template_name = 'Misc/NoviceChecklist.html'
class MiscLeaderChecklist(TemplateView):
    template_name = 'Misc/LeaderChecklist.html'

# Ardeche
class ArdecheAgas(TemplateView):
    template_name = 'Ardeche/Agas.html'
class ArdecheBarry(TemplateView):
    template_name = 'Ardeche/Barry.html'
class ArdecheBunis(TemplateView):
    template_name = 'Ardeche/Bunis.html'
class ArdecheCadet(TemplateView):
    template_name = 'Ardeche/Cadet.html'
class ArdecheCamilie(TemplateView):
    template_name = 'Ardeche/Camilie.html'
class ArdecheCentura(TemplateView):
    template_name = 'Ardeche/Centura.html'
class ArdecheChampclos(TemplateView):
    template_name = 'Ardeche/Champclos.html'
class ArdecheChataigniers(TemplateView):
    template_name = 'Ardeche/Chataigniers.html'
class ArdecheChazot(TemplateView):
    template_name = 'Ardeche/Chazot.html'
class ArdecheChenivesse(TemplateView):
    template_name = 'Ardeche/Chenivesse.html'
class ArdecheChevre(TemplateView):
    template_name = 'Ardeche/Chevre.html'
class ArdecheCombeRajeau(TemplateView):
    template_name = 'Ardeche/CombeRajeau.html'
class ArdecheCotepatiere(TemplateView):
    template_name = 'Ardeche/Cotepatiere.html'
class ArdecheCourtinen(TemplateView):
    template_name = 'Ardeche/Courtinen.html'
class ArdecheDerocs(TemplateView):
    template_name = 'Ardeche/Derocs.html'
class ArdecheDragonniere(TemplateView):
    template_name = 'Ardeche/Dragonniere.html'
class ArdecheFauxMarzal(TemplateView):
    template_name = 'Ardeche/FauxMarzal.html'
class ArdecheFontlongue(TemplateView):
    template_name = 'Ardeche/Fontlongue.html'
class ArdecheFoussoubie(TemplateView):
    template_name = 'Ardeche/Foussoubie.html'
class ArdecheGauthier(TemplateView):
    template_name = 'Ardeche/Gauthier.html'
class ArdecheGrandBadingue(TemplateView):
    template_name = 'Ardeche/GrandBadingue.html'
class ArdecheGregoire(TemplateView):
    template_name = 'Ardeche/Gregoire.html'
class ArdecheMarteau(TemplateView):
    template_name = 'Ardeche/Marteau.html'
class ArdecheNeufGorges(TemplateView):
    template_name = 'Ardeche/NeufGorges.html'
class ArdecheNoel(TemplateView):
    template_name = 'Ardeche/Noel.html'
class ArdechePebres(TemplateView):
    template_name = 'Ardeche/Pebres.html'
class ArdechePeyrejal(TemplateView):
    template_name = 'Ardeche/Peyrejal.html'
class ArdecheReynaud(TemplateView):
    template_name = 'Ardeche/Reynaud.html'
class ArdecheRichard(TemplateView):
    template_name = 'Ardeche/Richard.html'
class ArdecheRochas(TemplateView):
    template_name = 'Ardeche/Rochas.html'
class ArdecheRosa(TemplateView):
    template_name = 'Ardeche/Rosa.html'
class ArdecheRouveyrette(TemplateView):
    template_name = 'Ardeche/Rouveyrette.html'
class ArdecheStMarcel(TemplateView):
    template_name = 'Ardeche/StMarcel.html'
class ArdecheVarade(TemplateView):
    template_name = 'Ardeche/Varade.html'
class ArdecheVigneClose(TemplateView):
    template_name = 'Ardeche/VigneClose.html'
