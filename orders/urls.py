from django.urls import path
from orders.views import OrderAV,BuyerOrderSearch,ProviderOrderSearch

urlpatterns = [
    path("<int:pk>",OrderAV.as_view()),
    path("",OrderAV.as_view()),
    path("search/buyer/", BuyerOrderSearch.as_view(), name="order-search-buyer"),
    path("search/provider/", ProviderOrderSearch.as_view(), name="order-search-provider"),
]