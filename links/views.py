from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from links import serializers
from links.models import Link
from links.pagination import LinkPagination
from links.filters import LinkFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from links.models import Link   

class LinkAV(APIView):
    def get(self,request,pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response({"error":"Link not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.LinkSerializer(link)
        return Response(serializer.data)
    def put(self,request,pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response({"error":"Link not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.LinkSerializer(link,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    
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