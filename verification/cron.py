from .models import profile, recent_otp
from .otp import from_utc_to_local


def call_reset():
    obj = profile.objects.all()

    for i in obj:
        i.calls_left = 10
        i.save(update_fields=['calls_left'])

    obj = recent_otp.objects.all()
    
    for i in obj:
        if from_utc_to_local(i.date):
            i.delete()

