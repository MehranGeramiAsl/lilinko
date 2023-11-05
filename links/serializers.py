from rest_framework import serializers
from links.models import Link,LinkProvider,LinkCategories
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class LinkCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkCategories
        fields = ('id', 'title')

class LinkProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkProvider
        fields = ('id', 'provider', 'price', 'is_active')


class LinkSerializer(serializers.ModelSerializer):
    categories = LinkCategoriesSerializer(source='link', read_only=True,many=True)
    provider= LinkProviderSerializer(source='linkprovider_set', many=True, read_only=True)

    def extract_domain(self,url):
        url = url.replace("http://","")
        url = url.replace("https://","")
        url = url.replace("www.","")
        url = url.replace(" ","")
        url = "http://" + url
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain

    def validate_url(self,value):
        try:
            value = self.extract_domain(value)
        except Exception as e:
            print(e)
            raise serializers.ValidationError("Invalid URL. Please provide a valid internet URL.")
        return value
    
    
    class Meta:
        model = Link
        fields = "__all__"
        


