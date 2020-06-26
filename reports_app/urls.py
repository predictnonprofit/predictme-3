from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path("", ReportsListView.as_view(), name="reports-list-view"),
]
