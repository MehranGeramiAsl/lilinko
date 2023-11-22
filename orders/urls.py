from django.urls import path
from orders.views import OrderAV,OrderPriceAV,OrderSellerStatusAV,BuyerOrderList,ProviderOrderList

urlpatterns = [
    path("<int:pk>/price",OrderPriceAV.as_view()),
    path("<int:pk>/seller_status",OrderSellerStatusAV.as_view()),
    path("<int:pk>",OrderAV.as_view()),
    path("",OrderAV.as_view()),
    path("list/buyer/", BuyerOrderList.as_view(), name="order-list-buyer"),
    path("list/provider/", ProviderOrderList.as_view(), name="order-list-provider"),
]