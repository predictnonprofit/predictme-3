from django.urls import path
from .views import *
from data_handler.views import DataListView

urlpatterns = [
    path("", ProfileOverview.as_view(), name="profile-overview"),
    path("dashboard", ProfileDashboard.as_view(), name="profile-dashboard"),
    path("personal", ProfilePersonal.as_view(), name="profile-personal"),
    path("information", ProfileInformation.as_view(), name="profile-info"),
    path("change-password", ProfileChangePassword.as_view(), name="profile-change-password"),
    path("email", ProfileEmail.as_view(), name="profile-email"),
    path("data", DataListView.as_view(), name="data-list"),
    path("download", download_instructions_template, name='data-handler-temp-download'),
    path("download-excel", download_data_file_xlsx, name='data-handler-excel-download'),
    path("download-csv", download_data_file_csv, name='data-handler-csv-download'),
    path("download-dashboard", download_dashboard_pdf, name='profile-dashboard-download'),
]
