from django.urls import path, include
from .views import *

urlpatterns = [
    path("", UsersListView.as_view(), name="users-list"),
    path("create", UsersCreateView.as_view(), name="users-create"),
    path("details/<int:pk>", UsersDetailsView.as_view(), name="users-details"),
    path("list-pending", UsersPendingView.as_view(), name="users-pending"),
]