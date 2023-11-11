from django.urls import path
from orders.views import OrderAV,OrderSearch

urlpatterns = [
    path("<int:pk>",OrderAV.as_view()),
    path("",OrderAV.as_view()),
    path("search/",OrderSearch.as_view()),
]