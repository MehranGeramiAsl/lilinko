from django.urls import path
from links.views import LinkList,LinkSearch,LinkAV


urlpatterns = [
    path('list/',LinkList.as_view()),
    path('search/',LinkSearch.as_view()),
    path('<int:pk>',LinkAV.as_view())
]