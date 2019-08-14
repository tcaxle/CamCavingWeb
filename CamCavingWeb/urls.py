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

urlpatterns = [

    path('index.html', views.Home, name='Index'),

    # Admin
    path('Admin/', admin.site.urls),

    # User Portal
    path('Portal/', include('UserPortal.urls')),
    path('Portal/', include('django.contrib.auth.urls')),

    # Homepage
	path('', views.Home, name='Home'),

	# About
	path('About/Meets/', views.AboutMeetsFormatCost, name='AboutMeetsFormatCost'),
	path('About/TackleStore/', views.AboutTackleStore, name='AboutTackleStore'),
	path('About/Library/', views.AboutLibrary, name='AboutLibrary'),
	path('About/Constition&Safety/', views.AboutConstitutionSafety, name='AboutConstitutionSafety'),
	path('About/Expo/', views.AboutExpo, name='AboutExpo'),
    path('About/TripsAbroad/', views.AboutTripsAbroad, name='AboutTripsAbroad'),
    path('About/Bureaucracy/', views.AboutBureaucracy, name='AboutBureaucracy'),
    path('About/Archive/', views.AboutArchive, name='AboutArchive'),


	# Contact
	path('Contact/Committee/', views.ContactCommittee, name='ContactCommittee'),
	path('Contact/MailingList/', views.ContactMailingList, name='ContactMailingList'),

	# Meets
	path('Meets/Calendar/', views.MeetsCalendar, name='MeetsCalendar'),
	path('Meets/Blog/', views.MeetsBlog, name='MeetsBlog'),
	path('Meets/Pub/', views.MeetsPub, name='MeetsPub'),
	path('Meets/Social/', views.MeetsSocial, name='MeetsSocial'),
	path('Meets/Training/', views.MeetsTraining, name='MeetsTraining'),
    path('Meets/Dinners/', views.MeetsDinners, name='MeetsDinners'),

    # Gear
	path('Gear/FirstAid/', views.GearFirstAid, name='GearFirstAid'),
	path('Gear/Hire/', views.GearHire, name='GearHire'),
    path('Gear/Inventory/', views.GearInventory, name='GearInventory'),
    path('Gear/Tape/', views.GearTape, name='GearTape'),

	# Get Involved
	path('GetInvolved/HowToJoin/', views.GetInvolvedHowToJoin, name='GetInvolvedHowToJoin'),

    # Library
    path('Library/Books', views.LibraryBooks, name='LibraryBooks'),
    path('Library/MissingBooks', views.LibraryMissingBooks, name='LibraryMissingBooks'),

	# Misc
	path('Misc/CommitteeFunctions/', views.MiscCommitteeFunctions, name='MiscCommitteeFunctions'),
	path('Misc/NCAGuidelines/', views.MiscNCAGuidelines, name='MiscNCAGuidelines'),
    path('Misc/ExCS/', views.MiscExCS, name='MiscExCS'),
    path('Misc/NoviceChecklist/', views.MiscNoviceChecklist, name='MiscNoviceChecklist'),
    path('Misc/LeaderChecklist/', views.MiscLeaderChecklist, name='MiscLeaderChecklist'),


    # Ardheche
    path('Ardeche/Agas', views.ArdecheAgas, name='ArdecheAgas'),
    path('Ardeche/Barry', views.ArdecheBarry, name='ArdecheBarry'),
    path('Ardeche/Bunis', views.ArdecheBunis, name='ArdecheBunis'),
    path('Ardeche/Cadet', views.ArdecheCadet, name='ArdecheCadet'),
    path('Ardeche/Camilie', views.ArdecheCamilie, name='ArdecheCamilie'),
    path('Ardeche/Centura', views.ArdecheCentura, name='ArdecheCentura'),
    path('Ardeche/Champclos', views.ArdecheChampclos, name='ArdecheChampclos'),
    path('Ardeche/Chataigniers', views.ArdecheChataigniers, name='ArdecheChataigniers'),
    path('Ardeche/Chazot', views.ArdecheChazot, name='ArdecheChazot'),
    path('Ardeche/Chenivesse', views.ArdecheChenivesse, name='ArdecheChenivesse'),
    path('Ardeche/Chevre', views.ArdecheChevre, name='ArdecheChevre'),
    path('Ardeche/CombeRajeau', views.ArdecheCombeRajeau, name='ArdecheCombeRajeau'),
    path('Ardeche/Cotepatiere', views.ArdecheCotepatiere, name='ArdecheCotepatiere'),
    path('Ardeche/Courtinen', views.ArdecheCourtinen, name='ArdecheCourtinen'),
    path('Ardeche/Derocs', views.ArdecheDerocs, name='ArdecheDerocs'),
    path('Ardeche/Dragonniere', views.ArdecheDragonniere, name='ArdecheDragonniere'),
    path('Ardeche/FauxMarzal', views.ArdecheFauxMarzal, name='ArdecheFauxMarzal'),
    path('Ardeche/Fontlongue', views.ArdecheFontlongue, name='ArdecheFontlongue'),
    path('Ardeche/Foussoubie', views.ArdecheFoussoubie, name='ArdecheFoussoubie'),
    path('Ardeche/Gauthier', views.ArdecheGauthier, name='ArdecheGauthier'),
    path('Ardeche/GrandBadingue', views.ArdecheGrandBadingue, name='ArdecheGrandBadingue'),
    path('Ardeche/Gregoire', views.ArdecheGregoire, name='ArdecheGregoire'),
    path('Ardeche/Marteau', views.ArdecheMarteau, name='ArdecheMarteau'),
    path('Ardeche/NeufGorges', views.ArdecheNeufGorges, name='ArdecheNeufGorges'),
    path('Ardeche/Noel', views.ArdecheNoel, name='ArdecheNoel'),
    path('Ardeche/Pebres', views.ArdechePebres, name='ArdechePebres'),
    path('Ardeche/Peyrejal', views.ArdechePeyrejal, name='ArdechePeyrejal'),
    path('Ardeche/Reynaud', views.ArdecheReynaud, name='ArdecheReynaud'),
    path('Ardeche/Richard', views.ArdecheRichard, name='ArdecheRichard'),
    path('Ardeche/Rochas', views.ArdecheRochas, name='ArdecheRochas'),
    path('Ardeche/Rosa', views.ArdecheRosa, name='ArdecheRosa'),
    path('Ardeche/Rouveyrette', views.ArdecheRouveyrette, name='ArdecheRouveyrette'),
    path('Ardeche/StMarcel', views.ArdecheStMarcel, name='ArdecheStMarcel'),
    path('Ardeche/Varade', views.ArdecheVarade, name='ArdecheVarade'),
    path('Ardeche/VigneClose', views.ArdecheVigneClose, name='ArdecheVigneClose'),
]
