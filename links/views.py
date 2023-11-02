from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from links import serializers
from links.models import Link
from links.pagination import LinkPagination
from links.filters import LinkFilter


class LinkList(generics.ListAPIView):
    serializer_class = serializers.LinkSerializer
    pagination_class = LinkPagination

    def get_queryset(self):
        return Link.objects.all()


class LinkSearch(generics.ListAPIView):
    serializer_class = serializers.LinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinkFilter
    pagination_class = LinkPagination

    def get_queryset(self):
        queryset = Link.objects.all()
        return queryset