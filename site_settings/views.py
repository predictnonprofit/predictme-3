from django.shortcuts import render, reverse
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import (UpdateView)
from .forms import CompanySettingsForm
from django.contrib import messages
from django.urls import reverse_lazy



class CompanySettingsView(FormView):
    template_name = "site_settings/settings.html"
    form_class = CompanySettingsForm
    # success_url = reverse_lazy('site_settings:company-settings')
    success_url = reverse_lazy('company-settings')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # print(form.cleaned_data)
        print(form.cleaned_data.get("name"))
        return super().form_valid(form)


# def company_settings_view(request):
#     company_settings_form = CompanySettingsForm()
#     if request.method == "POST":
#         company_settings_form = CompanySettingsForm(request.POST)
#         print(company_settings_form)
#
#
#     return render(request, "site_settings/settings.html", context={"form": company_settings_form})

class AboutSettingsView(TemplateView):
    template_name = "site_settings/about.html"
