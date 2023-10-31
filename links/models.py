from django.db import models

# Create your models here.


class ProvidedLinks(models.Model):
    url = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255,blank=True,default=None)
    dr = models.SmallIntegerField()
    traffic = models.BigIntegerField()
    