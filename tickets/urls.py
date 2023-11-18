from django.urls import path
from tickets.views import TicketListAV


urlpatterns = [
    path('',TicketListAV.as_view())
]