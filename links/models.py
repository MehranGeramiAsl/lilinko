from django.db import models
from authentication.models import User
# Create your models here.


class Link(models.Model):
    url = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255,blank=True,default=None)
    dr = models.SmallIntegerField(default=0)
    traffic = models.BigIntegerField(default=0)

class LinkCategories(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class LinkProvider(models.Model):
    provider = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.ForeignKey(Link,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,null=False,blank=False)
    price = models.BigIntegerField(default=0)
