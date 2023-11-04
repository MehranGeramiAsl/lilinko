from django.db import models
from authentication.models import User


class Link(models.Model):
    url = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255,blank=True,default=None)
    dr = models.SmallIntegerField(default=0) # Field for domain rate
    traffic = models.BigIntegerField(default=0) # Field for storing traffic data

class LinkCategories(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.ManyToManyField(Link,related_name="link")
    # link_provider = models.ManyToManyField("LinkProvider",related_name="link_provider")


class LinkProvider(models.Model):
    provider = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.ForeignKey(Link,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,null=False,blank=False)
    price = models.BigIntegerField(default=0)


class LinkRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
    ("NS", "Not Specified"),
    ("A", "Accept"),
    ("R", "Reject"),
    ("PC", "Price Changed"),
    ("P", "Paied"),
    ]

    link_provider = models.ForeignKey(LinkProvider,on_delete=models.CASCADE)
    link = models.ForeignKey(Link,on_delete=models.CASCADE)
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="buyer")
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")
    seller_status = models.CharField(max_length=2,choices=REQUEST_STATUS_CHOICES,default="NS")
    buyer_status = models.CharField(max_length=2,choices=REQUEST_STATUS_CHOICES,default="NS")
    initial_price = models.BigIntegerField(default=0)
    updated_price = models.BigIntegerField(default=0)
    proposed_title = models.CharField(max_length=255,null=False,blank=False)
    proposed_content = models.TextField()
    backlink = models.CharField(max_length=255,null=False,blank=False)
    anchor_text = models.CharField(max_length=255,null=False,blank=False)
    proposed_meta_title = models.CharField(max_length=255,null=True,default=None)
    proposed_meta_description = models.CharField(max_length=255,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submited = models.BooleanField(default=False)