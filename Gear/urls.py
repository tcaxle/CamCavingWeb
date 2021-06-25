from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
	path('', RedirectView.as_view(url='/Gear/Hire/'), name='GearRedirect'),
	path('FirstAid/', views.GearFirstAid.as_view(), name='GearFirstAid'),
	path('Hire/', views.GearHire.as_view(), name='GearHire'),
    path('Tape/', views.GearTape.as_view(), name='GearTape'),

	# Signing in and out of gear
	path('SignOut/Rope/<int:pk>/', views.RopeSignOut, name='RopeSignOut'),
	path('SignIn/Rope/<int:pk>/', views.RopeSignIn, name='RopeSignIn'),

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

	# Adding and Editing Gear
	path('Add/Rope/', views.AddRope.as_view(), name='AddRope'),
	path('Edit/Rope/<int:pk>', views.EditRope.as_view(), name='EditRope'),
	path('Delete/Rope/<int:pk>', views.DeleteRope.as_view(), name='DeleteRope'),

	path('Add/Helmet/', views.AddHelmet.as_view(), name='AddHelmet'),
	path('Edit/Helmet/<int:pk>', views.EditHelmet.as_view(), name='EditHelmet'),
	path('Delete/Helmet/<int:pk>', views.DeleteHelmet.as_view(), name='DeleteHelmet'),

	path('Add/SRTKit/', views.AddSRTKit.as_view(), name='AddSRTKit'),
	path('Edit/SRTKit/<int:pk>', views.EditSRTKit.as_view(), name='EditSRTKit'),
	path('Delete/SRTKit/<int:pk>', views.DeleteSRTKit.as_view(), name='DeleteSRTKit'),

	path('Add/Harness/', views.AddHarness.as_view(), name='AddHarness'),
	path('Edit/Harness/<int:pk>', views.EditHarness.as_view(), name='EditHarness'),
	path('Delete/Harness/<int:pk>', views.DeleteHarness.as_view(), name='DeleteHarness'),

	path('Add/Undersuit/', views.AddUndersuit.as_view(), name='AddUndersuit'),
	path('Edit/Undersuit/<int:pk>', views.EditUndersuit.as_view(), name='EditUndersuit'),
	path('Delete/Undersuit/<int:pk>', views.DeleteUndersuit.as_view(), name='DeleteUndersuit'),

	path('Add/Oversuit/', views.AddOversuit.as_view(), name='AddOversuit'),
	path('Edit/Oversuit/<int:pk>', views.EditOversuit.as_view(), name='EditOversuit'),
	path('Delete/Oversuit/<int:pk>', views.DeleteOversuit.as_view(), name='DeleteOversuit'),

	path('Add/OtherGear/', views.AddOtherGear.as_view(), name='AddOtherGear'),
	path('Edit/OtherGear/<int:pk>', views.EditOtherGear.as_view(), name='EditOtherGear'),
	path('Delete/OtherGear/<int:pk>', views.DeleteOtherGear.as_view(), name='DeleteOtherGear'),

	path('ViewHires/Rope/', views.ViewHiresRope.as_view(), name='ViewHiresRope'),
	path('ViewHires/Helmet/', views.ViewHiresHelmet.as_view(), name='ViewHiresHelmet'),
	path('ViewHires/SRTKit/', views.ViewHiresSRTKit.as_view(), name='ViewHiresSRTKit'),
	path('ViewHires/Harness/', views.ViewHiresHarness.as_view(), name='ViewHiresHarness'),
	path('ViewHires/Undersuit/', views.ViewHiresUndersuit.as_view(), name='ViewHiresUndersuit'),
	path('ViewHires/Oversuit/', views.ViewHiresOversuit.as_view(), name='ViewHiresOversuit'),
	path('ViewHires/OtherGear/', views.ViewHiresOtherGear.as_view(), name='ViewHiresOtherGear'),
]
