from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path("", ReportsListView.as_view(), name="reports-list-view"),
    path("users", ReportsUsersListView.as_view(), name="reports-users-list-view"),
    path("data-usage", ReportsDataUsageView.as_view(), name="reports-data-usage-list-view"),
    path("extra-records", ReportsExtraUsageView.as_view(), name="reports-extra-usage-list-view"),
    path("profit-share", ProfitShareView.as_view(), name="reports-profit-share-list-view"),
    path("revenues", ReportsRevenuesView.as_view(), name="reports-revenues"),
]
