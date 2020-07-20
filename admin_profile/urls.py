from django.urls import path, include
from .views import *

urlpatterns = [
    path("", ProfileOverview.as_view(), name="profile-overview"),
    path("personal", ProfilePersonal.as_view(), name="profile-personal"),
    path("information", ProfileInformation.as_view(), name="profile-info"),
    path("change-password", ProfileChangePassword.as_view(), name="profile-change-password"),
    path("email", ProfileEmail.as_view(), name="profile-email"),
]