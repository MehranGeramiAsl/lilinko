from django.shortcuts import render
from rest_framework import generics

from links import serializers
from links.models import Link
from links import pagination

class LinkList(generics.ListAPIView):
    serializer_class = serializers.LinkSerializer
    # pagination_class = [pagination.LinkPagination]

    def get_queryset(self):
        return Link.objects.all()
