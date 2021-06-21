import requests
import random
import time
from .models import recent_otp

url = 'https://2factor.in/API/V1/8088caf5-fdbd-11ea-9fa5-0200cd936042/SMS/+91'
char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def generate_username():
    l = random.randint(8, 14)
    username = ''

    for i in range(l):
        username += char[random.randint(0, 62)]
    return username


def random_num():
    otp = 0
    for i in range(6):
        otp = 10 * otp + random.randint(0, 9)
        if otp == 0:
            otp = 1
    return otp


def generate_otp(num):
    otp = random_num()
    return str(otp)
    try:
        req = requests.get(url=url + num + '/' + str(otp))
        req = req.json()
        if req['Status'] == 'Success':
            return str(otp)
        else:
            return '-1'
    except requests.RequestException:
        return '-1'


def from_utc_to_local(offset):
    t1 = (time.time() - offset)
    if t1 > 120:
        return True
    else:
        return False


def update_otp(mob, otp):
    try:
        otpObj = recent_otp.objects.get(phone=mob)
        otpObj.otp = str(otp)
        otpObj.date = time.time()
        otpObj.save(update_fields=['otp', 'date'])
    except recent_otp.DoesNotExist:
        otpObj = recent_otp.objects.create(phone=mob, otp=str(otp), date=time.time())
        otpObj.save()


def get_otp(mob, otp):
    try:
        otpObj = recent_otp.objects.get(phone=mob)
        return otpObj.otp == otp and not from_utc_to_local(otpObj.date)

    except recent_otp.DoesNotExist:
        return False
