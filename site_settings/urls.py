from django.urls import path
from .views import *

urlpatterns = [
    # path("company", company_settings_view, name="company-settings"),
    path("company", CompanySettingsView.as_view(), name="company-settings"),
    path("about", AboutSettingsView.as_view(), name="site-about"),

]