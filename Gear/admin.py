from django.contrib import admin
from .models import *

admin.site.register(Rope)
admin.site.register(HireRope)

admin.site.register(Helmet)
admin.site.register(HireHelmet)

admin.site.register(SRTKit)
admin.site.register(HireSRTKit)

admin.site.register(Harness)
admin.site.register(HireHarness)

admin.site.register(Undersuit)
admin.site.register(HireUndersuit)

admin.site.register(Oversuit)
admin.site.register(HireOversuit)

admin.site.register(OtherGear)
admin.site.register(SignOutOtherGear)
admin.site.register(SignInOtherGear)
