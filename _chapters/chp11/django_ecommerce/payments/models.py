from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    #password field defined in base class
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @classmethod
    def get_by_id(cls, uid):
        return User.objects.get(pk=uid)

    @classmethod
    def create(cls, name, email, password, last_4_digits, stripe_id=''):
        new_user = cls(name=name, email=email,
                       last_4_digits=last_4_digits, stripe_id=stripe_id)
        new_user.set_password(password)

        new_user.save()
        return new_user


class UnpaidUsers(models.Model):
    email = models.CharField(max_length=255, unique=True)
    last_notification = models.DateTimeField(default=datetime.now())
