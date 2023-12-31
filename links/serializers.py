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
    categories = LinkCategoriesSerializer(many=True,read_only=True)
    provider= LinkProviderSerializer(source='linkprovider_set', many=True,read_only=True)


    def create(self,validated_data):
        provider = validated_data.pop('provider', None)
        price = validated_data.pop('price',0)
        categories = validated_data.pop('categories',None)
        link, created = Link.objects.get_or_create(url=validated_data['url'])
        link_provider, provider_created = LinkProvider.objects.get_or_create(
            link=link,
            provider=provider,
            defaults={'price': price}
        )
        for category in categories:
            link.categories.add(category)
        return link
    
    def update(self,link,validated_data):
        price = validated_data.pop('price',0)
        provider = validated_data.pop('provider', None)
        if provider != None:
            link_provider = LinkProvider.objects.filter(provider=provider,link=link)
            if link_provider.exists():
                link_provider = link_provider.first()
                link_provider.price = price
                link_provider.save()
                return link
            else:
                LinkProvider.objects.create(provider=provider,link=link,price=price)
                return link

    
        price = validated_data.pop('price',0)
        provider = validated_data.pop('provider', None)
        link_provider = LinkProvider.objects.filter(provider=provider,link=link)
        if link_provider.exists():
            link_provider = link_provider.first()
            link_provider.price = price
            link_provider.save()
            return link
        else:
            LinkProvider.objects.create(provider=provider,link=link,price=price)
            return link
    
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
        


class LinkListSerializer(serializers.ModelSerializer):
    categories = LinkCategoriesSerializer(many=True,read_only=True)
    provider= LinkProviderSerializer(source='linkprovider_set', many=True,write_only=True)
    class Meta:
        model = Link
        fields = "__all__"
        
