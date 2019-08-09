from django.urls import path
from . import views

urlpatterns = [
	# Homepage
	path('', views.index, name='index'),

	# About Section
	path('About/Meets/', views.AboutMeetsFormatCost, name='AboutMeetsFormatCost'),
	path('About/TackleStore/', views.AboutTackleStore, name='AboutTackleStore'),
	path('About/Library/', views.AboutLibrary, name='AboutLibrary'),
	path('About/Constition&Safety/', views.AboutConstitutionSafety, name='AboutConstitutionSafety'),

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
