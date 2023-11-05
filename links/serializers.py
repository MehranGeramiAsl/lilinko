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
    
    def validate_url(self,value):
        try:
            value = urlparse(value)
            print(value)
            value = value.path
            value = value.replace("/","")
            value = value.replace("\\","")
        except Exception as e:
            print(e)
            raise serializers.ValidationError("Invalid URL. Please provide a valid internet URL.")
        return value
    class Meta:
        model = Link
        fields = "__all__"

    # def get_categories(self, obj):
    #     # Fetch and serialize LinkCategories related to the current Link object
    #     categories = obj.linkcategories_set.all()
    #     serializer = LinkCategoriesSerializer(categories, many=True)
    #     return serializer.data
