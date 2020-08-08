from django.urls import path, include
from .views import *
from data_handler.views import (DataListView, session_details, SessionDetailsView)

urlpatterns = [
    path("", ProfileOverview.as_view(), name="profile-overview"),
    path("dashboard", ProfileDashboard.as_view(), name="profile-dashboard"),
    path("personal", ProfilePersonal.as_view(), name="profile-personal"),
    path("information", ProfileInformation.as_view(), name="profile-info"),
    path("change-password", ProfileChangePassword.as_view(), name="profile-change-password"),
    path("email", ProfileEmail.as_view(), name="profile-email"),
    path("data/", include([
        path("", DataListView.as_view(), name='data-handler-default'),
        path("<int:id>/", SessionDetailsView.as_view(), name='data-handler-session-details'),
    ]), name="data-list"),

    path("download", download_instructions_template, name='data-handler-temp-download'),
    path("download-excel/<int:id>", download_data_file_xlsx, name='data-handler-excel-download'),
    path("download-csv/<int:id>", download_data_file_csv, name='data-handler-csv-download'),
    path("download-dashboard", download_dashboard_pdf, name='profile-dashboard-download'),
]
