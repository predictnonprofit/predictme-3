from django.urls import path, re_path
from .views import *

urlpatterns = [
    # path("list", DataListView.as_view(), name="data-list"),
    path("init", data_handler_init, name="data-handler-init"),
    path("download", download_instructions_template, name='data-handler-temp-download'),
    path("test_box", data_handler_test_dual, name="data-handler-test-dual"),
    re_path("^upload/(?P<filename>[^/]+)$", DataHandlerFileUpload.as_view(), name="data-handler-upload"),
    path("api/save-columns", SaveColumnsView.as_view(), name="data-handler-save-columns-names"),
    path("api/get-columns", GetColumnsView.as_view(), name="data-handler-get-columns"),
    path("api/get-all-columns", GetAllColumnsView.as_view(), name="data-handler-get-all-columns"),
    path("api/rows", GetRowsView.as_view(), name="data-handler-rows"),
    path("api/save-rows", SaveNewRowsUpdateView.as_view(), name="data-handler-save-rows"),
    path("api/delete-file", DeleteDataFileView.as_view(), name="data-handler-delete-file"),
    path("api/validate-columns", ValidateColumnsView.as_view(), name="data-handler-validate-columns"),

]
