from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("list", DataListView.as_view(), name="data-list"),
    path("init", data_handler_init, name="data-handler-init"),
    # path("upload", data_handler_file_upload, name="data-handler-upload"),
    re_path("^upload/(?P<filename>[^/]+)$", DataHandlerFileUpload.as_view(), name="data-handler-upload"),
    path("records", RecordsColumnView.as_view(), name="data-handler-records"),
]