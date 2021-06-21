from django.contrib import admin
from django.contrib.auth.models import Group
from verification.models import profile, recent_otp


admin.site.unregister(Group)
admin.site.register(profile)
admin.site.register(recent_otp)
