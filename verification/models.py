from django.db import models
import time
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, phone, username, password='a@for@apple',  admin=True):
        obj = self.model(
            phone=phone
        )
        obj.set_password(password)
        obj.username = username
        obj.calls_left = 10
        obj.active = True
        obj.admin = admin
        obj.save(using=self._db)
        return obj

    def create_superuser(self, phone, username='admin', password='a@for@apple'):

        user = self.create_user(
            phone=phone,
            password=password,
            username=username,
        )
        user.calls_left = 10
        user.active = True
        user.admin = True
        user.save(using=self._db)
        return user


class profile(AbstractBaseUser):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=10, blank=False, null=False, unique= True)
    calls_left = models.IntegerField(default=10, blank=False, null=False)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj= None):
        return True


class recent_otp(models.Model):
    phone = models.CharField(max_length=10, blank=False, null=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    date = models.FloatField(default=time.time(), blank=False, null=False)

    def __str__(self):
        return self.phone
