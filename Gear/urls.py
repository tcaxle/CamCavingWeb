from django.urls import path
from . import views

urlpatterns = [
	path('FirstAid/', views.GearFirstAid.as_view(), name='GearFirstAid'),
	path('Hire/', views.GearHire.as_view(), name='GearHire'),
    path('Inventory/', views.GearInventory.as_view(), name='GearInventory'),
    path('Tape/', views.GearTape.as_view(), name='GearTape'),

	# Signing in and out of gear 
	path('SignOut/Rope/<int:pk>', views.RopeSignOut, name='RopeSignOut'),
	path('SignIn/Rope/<int:pk>', views.RopeSignIn, name='RopeSignIn'),
]
