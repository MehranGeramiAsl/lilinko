from django.urls import path
from links.views import LinkList


urlpatterns = [
    path('list',LinkList.as_view())
]