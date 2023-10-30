from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255,unique=True,null=True,blank=True)
    phone = models.CharField(max_length=17,unique=True,null=True,blank=True)
    tfa_secret = models.CharField(max_length=255,default='')
    otp = models.CharField(max_length=255,default=None)
    otp_date = models.DateTimeField(auto_now=True)
    otp_used = models.BooleanField(default=True)
