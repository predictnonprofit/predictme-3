from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    # path("list", DataListView.as_view(), name="data-list"),
    path("init", data_handler_init, name="data-handler-init"),
    # path("test_box", data_handler_test_dual, name="data-handler-test-dual"),
    re_path("^upload/(?P<filename>[^/]+)$", DataHandlerFileUpload.as_view(), name="data-handler-upload"),
    path("api/", include([
        path("save-columns", SaveColumnsView.as_view(), name="data-handler-save-columns-names"),
        path("get-columns", GetColumnsView.as_view(), name="data-handler-get-columns"),
        path("get-all-columns", GetAllColumnsView.as_view(), name="data-handler-get-all-columns"),
        path("rows", GetRowsView.as_view(), name="data-handler-rows"),
        path("search-query-records", GetRowsBySearchQueryView.as_view(), name="data-handler-search-rows"),
        path("not-validate-rows", NotValidateRowsView.as_view(), name="data-handler-not-validate-rows"),
        path("update-rows", SaveNewRowsUpdateView.as_view(), name="data-handler-update-rows"),
        path("delete-file", DeleteDataFileView.as_view(), name="data-handler-delete-file"),
        path("validate-columns", ValidateColumnsView.as_view(), name="data-handler-validate-columns"),
        path("filter-rows", FilterRowsView.as_view(), name="data-handler-filter-rows"),
        path("accepts-download", AcceptsDownload.as_view(), name="data-handler-accepts-download"),
        path("check-upload-member", CheckMemberUpload.as_view(), name="data-handler-check-upload-member"),
        path("check-process-status", CheckMemberProcessStatus.as_view(), name="data-handler-check-process-status"),
        path("fetch-last-session-name", FetchLastSessionNameView.as_view(), name="data-handler-fetch-last-session-name"),
        path("set-last-session-name", SetLastSessionName.as_view(), name="data-handler-set-last-session-name"),
        path("set-session-label", SetSessionLabel.as_view(), name="data-handler-set-session-label"),
    ])),


]
