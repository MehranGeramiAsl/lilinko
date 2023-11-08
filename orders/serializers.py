from rest_framework import serializers
from orders.models import LinkOrder
from links.serializers import LinkProviderSerializer

 

class OrderSerializer(serializers.ModelSerializer):
    link_provider = LinkProviderSerializer(read_only=True)
    class Meta:
        model = LinkOrder
        fields = "__all__"