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

	path('SignOut/Helmet/<int:pk>', views.HelmetSignOut, name='HelmetSignOut'),
	path('SignIn/Helmet/<int:pk>', views.HelmetSignIn, name='HelmetSignIn'),

	path('SignOut/SRT/<int:pk>', views.SRTKitSignOut, name='SRTKitSignOut'),
	path('SignIn/SRT/<int:pk>', views.SRTKitSignIn, name='SRTKitSignIn'),

	path('SignOut/Harness/<int:pk>', views.HarnessSignOut, name='HarnessSignOut'),
	path('SignIn/Harness/<int:pk>', views.HarnessSignIn, name='HarnessSignIn'),

	path('SignOut/Undersuit/<int:pk>', views.UndersuitSignOut, name='UndersuitSignOut'),
	path('SignIn/Undersuit/<int:pk>', views.UndersuitSignIn, name='UndersuitSignIn'),

	path('SignOut/Oversuit/<int:pk>', views.OversuitSignOut, name='OversuitSignOut'),
	path('SignIn/Oversuit/<int:pk>', views.OversuitSignIn, name='OversuitSignIn'),

	path('SignOut/OtherGear/<int:pk>', views.OtherGearSignOut, name='OtherGearSignOut'),
	path('SignIn/OtherGear/<int:pk>', views.OtherGearSignIn, name='OtherGearSignIn'),
]
