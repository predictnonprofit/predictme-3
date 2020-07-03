from django.urls import path, re_path
from .views import *

urlpatterns = [
    # path("list", DataListView.as_view(), name="data-list"),
    path("init", data_handler_init, name="data-handler-init"),
    path("test_box", data_handler_test_dual, name="data-handler-test-dual"),
    re_path("^upload/(?P<filename>[^/]+)$", DataHandlerFileUpload.as_view(), name="data-handler-upload"),
    path("api/save-columns", SaveColumnsView.as_view(), name="data-handler-save-columns-names"),
    path("api/get-columns", GetColumnsView.as_view(), name="data-handler-get-columns"),
    path("api/get-all-columns", GetAllColumnsView.as_view(), name="data-handler-get-all-columns"),
    path("api/rows", GetRowsView.as_view(), name="data-handler-rows"),
    path("api/search-query-records", GetRowsBySearchQueryView.as_view(), name="data-handler-search-rows"),
    path("api/not-validate-rows", NotValidateRowsView.as_view(), name="data-handler-not-validate-rows"),
    path("api/update-rows", SaveNewRowsUpdateView.as_view(), name="data-handler-update-rows"),
    path("api/delete-file", DeleteDataFileView.as_view(), name="data-handler-delete-file"),
    path("api/validate-columns", ValidateColumnsView.as_view(), name="data-handler-validate-columns"),
    path("api/filter-rows", FilterRowsView.as_view(), name="data-handler-filter-rows"),
    path("api/accepts-download", AcceptsDownload.as_view(), name="data-handler-accepts-download"),
    path("api/check-upload-member", CheckMemberUpload.as_view(), name="data-handler-check-upload-member"),

]
