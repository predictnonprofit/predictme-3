from django.urls import path
from .views import *

urlpatterns = [
    path("list", DataListView.as_view(), name="data-list"),
]