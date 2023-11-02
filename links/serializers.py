from rest_framework import serializers
from links.models import Link,LinkProvider,LinkCategories


class LinkCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkCategories
        fields = ('id', 'title')

class LinkProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkProvider
        fields = ('id', 'provider', 'price', 'is_active')


class LinkSerializer(serializers.ModelSerializer):
    provider= LinkProviderSerializer(source='linkprovider_set', many=True, read_only=True)
    categories = LinkCategoriesSerializer(many=True, read_only=True)
    class Meta:
        model = Link
        fields = "__all__"