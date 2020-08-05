from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path("", ReportsListView.as_view(), name="reports-list-view"),
    path("users", ReportsUsersListView.as_view(), name="reports-users-list-view"),
    path("data_usage", ReportsDataUsageView.as_view(), name="reports-data-usage-list-view"),
    path("extra_record", ReportsExtraUsageView.as_view(), name="reports-extra-usage-list-view"),
    path("revenues", ReportsRevenuesView.as_view(), name="reports-revenues"),
]
