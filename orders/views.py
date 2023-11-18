from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from orders import serializers
from orders.models import LinkOrder
from orders.pagination import OrderPagination
from orders.filters import OrderFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from links.models import Link   
from authentication.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from orders.permissions import IsBuyerOrSeller,IsBuyer


class OrderAV(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsBuyerOrSeller()]
        elif self.request.method == 'PUT':
            return [IsAuthenticated(), IsBuyer()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBuyer()]
        return [IsAuthenticated()]

    def get(self,request,pk):
        try:
            order = LinkOrder.objects.get(pk=pk)
        except LinkOrder.DoesNotExist:
            return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
    
    def post(self,request):
        # data = request.data.copy()
        buyer = request.user.id
        try:
            link_provider = request.data["link_provider"]
        except Exception as e:
            raise serializers.serializers.ValidationError({"success":False,"errors":e})
        
        print(link_provider)

        # url = data['url']
        try:
            # order = Link.objects.get(url=url)
        
            serializer = serializers.OrderSerializer(data=request.data)
        except Exception as e:
            print(e)
        if serializer.is_valid():
            
            serializer.save(buyer = buyer,link_provider=link_provider)
            return Response({"success":True,"data":serializer.data})
        else:
            return Response({"success":False,"errors":serializer.errors})
        
    
    def put(self,request,pk):
        try:
            order = LinkOrder.objects.get(pk=pk)
        except order.DoesNotExist:
            return Response({"success":False,"errors":"Order not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.OrderSerializer(order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            link = LinkOrder.objects.get(id=pk)
            link.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

class BuyerOrderList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    # pagination_class = OrderPagination

    def get_queryset(self):
        user = self.request.user
        queryset = LinkOrder.objects.filter(buyer=user)
        return queryset


class ProviderOrderList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    # pagination_class = OrderPagination

    def get_queryset(self):
        user = self.request.user
        queryset = LinkOrder.objects.filter(link_provider__provider=user)
        return queryset

    