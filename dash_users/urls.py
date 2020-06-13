from django.urls import path, include
from .views import *

urlpatterns = [
    path("", UsersListView.as_view(), name="users-list"),
    path("create", UsersCreateView.as_view(), name="users-create"),
    path("list-pending", UsersPendingView.as_view(), name="users-pending"),
]