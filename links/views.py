from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from links import serializers
from links.models import Link,LinkProvider
from links.pagination import LinkPagination
from links.filters import LinkFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from links.models import Link   
from authentication.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class LinkAV(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response({"error":"Link not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.LinkSerializer(link)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data.copy()
        data['provider'] = request.user.id
        url = data['url']
        try:
            link = Link.objects.get(url=url)
            serializer = serializers.LinkSerializer(link,data=data)
        except:
            serializer = serializers.LinkSerializer(data=data)
        if serializer.is_valid():
            serializer.save(provider = request.user,categories = data["categories"],price = data["price"])
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
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
    
    def delete(self,request,pk):
        try:
            link = Link.objects.get(id=pk)
            link.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

    
    
class LinkList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LinkListSerializer
    pagination_class = LinkPagination

    def get_queryset(self):
        user = self.request.user
        link_providers = LinkProvider.objects.filter(provider=user)
        links_for_provider = link_providers.values_list('link')
        queryset = Link.objects.filter(pk__in=links_for_provider)
        return queryset


class LinkSearch(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinkFilter
    pagination_class = LinkPagination

    def get_queryset(self):
        queryset = Link.objects.all()
        return queryset