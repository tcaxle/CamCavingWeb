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

	# Gear Section

	# Meets Section

	# Get Involved Section

]
