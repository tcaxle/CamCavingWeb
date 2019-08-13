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

    # Admin
    path('Admin/', admin.site.urls),

    # User Portal
    path('Portal/', include('UserPortal.urls')),
    path('Portal/', include('django.contrib.auth.urls')),

    # Homepage
	path('', views.Home, name='Home'),

	# About Section
	path('About/Meets/', views.AboutMeetsFormatCost, name='AboutMeetsFormatCost'),
	path('About/TackleStore/', views.AboutTackleStore, name='AboutTackleStore'),
	path('About/Library/', views.AboutLibrary, name='AboutLibrary'),
	path('About/Constition&Safety/', views.AboutConstitutionSafety, name='AboutConstitutionSafety'),
	path('About/Expo/', views.AboutExpo, name='AboutExpo'),
    path('About/Bureaucracy/', views.AboutBureaucracy, name='AboutBureaucracy'),
    path('About/Archive/', views.AboutArchive, name='AboutArchive'),


	# Contact Section
	path('Contact/Committee/', views.ContactCommittee, name='ContactCommittee'),
	path('Contact/MailingList/', views.ContactMailingList, name='ContactMailingList'),

	# Meets Section
	path('Meets/Calendar/', views.MeetsCalendar, name='MeetsCalendar'),
	path('Meets/Blog/', views.MeetsBlog, name='MeetsBlog'),
	path('Meets/Pub/', views.MeetsPub, name='MeetsPub'),
	path('Meets/Social/', views.MeetsSocial, name='MeetsSocial'),
	path('Meets/Training/', views.MeetsTraining, name='MeetsTraining'),

	# Get Involved Section
	path('GetInvolved/HowToJoin/', views.GetInvolvedHowToJoin, name='GetInvolvedHowToJoin'),
]
