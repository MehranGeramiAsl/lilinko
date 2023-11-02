from django.urls import path
from links.views import LinkList,LinkSearch


urlpatterns = [
    path('list/',LinkList.as_view()),
    path('search/',LinkSearch.as_view()),
]