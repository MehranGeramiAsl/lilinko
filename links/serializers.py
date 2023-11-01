from rest_framework import serializers
from links.models import Link

class LinkSerializer(serializers.ModelSerializer):
    link = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Link
        fields = "__all__"