"""CamCavingWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    # Includes
    path('Portal/', include('UserPortal.urls')),
    path('Portal/', include('django.contrib.auth.urls')),
    path('Blog/', include('Blog.urls')),
    path('Admin/', admin.site.urls),

    # Redirects
    path('index.html/', views.Home.as_view(), name='IndexRedirect'),
    path('accounts/login/', RedirectView.as_view(url='/Portal/login/'), name='LoginRedirect'),

    # Homepage
	path('', views.Home.as_view(), name='Home'),

	# About
	path('About/Meets/', views.AboutMeetsFormatCost.as_view(), name='AboutMeetsFormatCost'),
	path('About/TackleStore/', views.AboutTackleStore.as_view(), name='AboutTackleStore'),
	path('About/Library/', views.AboutLibrary.as_view(), name='AboutLibrary'),
	path('About/Constition&Safety/', views.AboutConstitutionSafety.as_view(), name='AboutConstitutionSafety'),
	path('About/Expo/', views.AboutExpo.as_view(), name='AboutExpo'),
    path('About/TripsAbroad/', views.AboutTripsAbroad.as_view(), name='AboutTripsAbroad'),
    path('About/Bureaucracy/', views.AboutBureaucracy.as_view(), name='AboutBureaucracy'),

	# Contact
	path('Contact/Committee/', views.ContactCommittee.as_view(), name='ContactCommittee'),
	path('Contact/MailingList/', views.ContactMailingList.as_view(), name='ContactMailingList'),

	# Meets
	path('Meets/Calendar/', views.MeetsCalendar.as_view(), name='MeetsCalendar'),
	path('Meets/Pub/', views.MeetsPub.as_view(), name='MeetsPub'),
    path('Meets/Caving/', views.MeetsCaving.as_view(), name='MeetsCaving'),
	path('Meets/Social/', views.MeetsSocial.as_view(), name='MeetsSocial'),
	path('Meets/Training/', views.MeetsTraining.as_view(), name='MeetsTraining'),
    path('Meets/Dinners/', views.MeetsDinners.as_view(), name='MeetsDinners'),

    # Gear
	path('Gear/FirstAid/', views.GearFirstAid.as_view(), name='GearFirstAid'),
	path('Gear/Hire/', views.GearHire.as_view(), name='GearHire'),
    path('Gear/Inventory/', views.GearInventory.as_view(), name='GearInventory'),
    path('Gear/Tape/', views.GearTape.as_view(), name='GearTape'),

	# Get Involved
	path('GetInvolved/HowToJoin/', views.GetInvolvedHowToJoin.as_view(), name='GetInvolvedHowToJoin'),

    # Library
    path('Library/Books', views.LibraryBooks.as_view(), name='LibraryBooks'),
    path('Library/MissingBooks', views.LibraryMissingBooks.as_view(), name='LibraryMissingBooks'),

	# Misc
	path('Misc/CommitteeFunctions/', views.MiscCommitteeFunctions.as_view(), name='MiscCommitteeFunctions'),
	path('Misc/NCAGuidelines/', views.MiscNCAGuidelines.as_view(), name='MiscNCAGuidelines'),
    path('Misc/ExCS/', views.MiscExCS.as_view(), name='MiscExCS'),
    path('Misc/NoviceChecklist/', views.MiscNoviceChecklist.as_view(), name='MiscNoviceChecklist'),
    path('Misc/LeaderChecklist/', views.MiscLeaderChecklist.as_view(), name='MiscLeaderChecklist'),


    # Ardheche
    path('Ardeche/Agas', views.ArdecheAgas.as_view(), name='ArdecheAgas'),
    path('Ardeche/Barry', views.ArdecheBarry.as_view(), name='ArdecheBarry'),
    path('Ardeche/Bunis', views.ArdecheBunis.as_view(), name='ArdecheBunis'),
    path('Ardeche/Cadet', views.ArdecheCadet.as_view(), name='ArdecheCadet'),
    path('Ardeche/Camilie', views.ArdecheCamilie.as_view(), name='ArdecheCamilie'),
    path('Ardeche/Centura', views.ArdecheCentura.as_view(), name='ArdecheCentura'),
    path('Ardeche/Champclos', views.ArdecheChampclos.as_view(), name='ArdecheChampclos'),
    path('Ardeche/Chataigniers', views.ArdecheChataigniers.as_view(), name='ArdecheChataigniers'),
    path('Ardeche/Chazot', views.ArdecheChazot.as_view(), name='ArdecheChazot'),
    path('Ardeche/Chenivesse', views.ArdecheChenivesse.as_view(), name='ArdecheChenivesse'),
    path('Ardeche/Chevre', views.ArdecheChevre.as_view(), name='ArdecheChevre'),
    path('Ardeche/CombeRajeau', views.ArdecheCombeRajeau.as_view(), name='ArdecheCombeRajeau'),
    path('Ardeche/Cotepatiere', views.ArdecheCotepatiere.as_view(), name='ArdecheCotepatiere'),
    path('Ardeche/Courtinen', views.ArdecheCourtinen.as_view(), name='ArdecheCourtinen'),
    path('Ardeche/Derocs', views.ArdecheDerocs.as_view(), name='ArdecheDerocs'),
    path('Ardeche/Dragonniere', views.ArdecheDragonniere.as_view(), name='ArdecheDragonniere'),
    path('Ardeche/FauxMarzal', views.ArdecheFauxMarzal.as_view(), name='ArdecheFauxMarzal'),
    path('Ardeche/Fontlongue', views.ArdecheFontlongue.as_view(), name='ArdecheFontlongue'),
    path('Ardeche/Foussoubie', views.ArdecheFoussoubie.as_view(), name='ArdecheFoussoubie'),
    path('Ardeche/Gauthier', views.ArdecheGauthier.as_view(), name='ArdecheGauthier'),
    path('Ardeche/GrandBadingue', views.ArdecheGrandBadingue.as_view(), name='ArdecheGrandBadingue'),
    path('Ardeche/Gregoire', views.ArdecheGregoire.as_view(), name='ArdecheGregoire'),
    path('Ardeche/Marteau', views.ArdecheMarteau.as_view(), name='ArdecheMarteau'),
    path('Ardeche/NeufGorges', views.ArdecheNeufGorges.as_view(), name='ArdecheNeufGorges'),
    path('Ardeche/Noel', views.ArdecheNoel.as_view(), name='ArdecheNoel'),
    path('Ardeche/Pebres', views.ArdechePebres.as_view(), name='ArdechePebres'),
    path('Ardeche/Peyrejal', views.ArdechePeyrejal.as_view(), name='ArdechePeyrejal'),
    path('Ardeche/Reynaud', views.ArdecheReynaud.as_view(), name='ArdecheReynaud'),
    path('Ardeche/Richard', views.ArdecheRichard.as_view(), name='ArdecheRichard'),
    path('Ardeche/Rochas', views.ArdecheRochas.as_view(), name='ArdecheRochas'),
    path('Ardeche/Rosa', views.ArdecheRosa.as_view(), name='ArdecheRosa'),
    path('Ardeche/Rouveyrette', views.ArdecheRouveyrette.as_view(), name='ArdecheRouveyrette'),
    path('Ardeche/StMarcel', views.ArdecheStMarcel.as_view(), name='ArdecheStMarcel'),
    path('Ardeche/Varade', views.ArdecheVarade.as_view(), name='ArdecheVarade'),
    path('Ardeche/VigneClose', views.ArdecheVigneClose.as_view(), name='ArdecheVigneClose'),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
