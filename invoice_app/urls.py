from django.urls import path
from .views import *

urlpatterns = [
    path("details", InvoiceDetailsView.as_view(), name="invoice-details"),
    path("list", InvliceListView.as_view(), name="invoice-list"),
    path("create", InvCreateView.as_view(), name="invoice-create"),
    path("print", InvoicePrintView.as_view(), name='invoice-print'),
    # path("download", InvoiceDownloadView.as_view(), name='invoice-download'),

]