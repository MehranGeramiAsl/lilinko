from django.urls import path
from orders.views import OrderAV

urlpatterns = [
    path("<int:pk>",OrderAV.as_view()),
    path("",OrderAV.as_view())
]