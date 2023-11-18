from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from authentication.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from tickets.models import Ticket
# Create your views here.


class TicketListAV(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(owner = user)
        return queryset

    