from django.shortcuts import (render, reverse, get_object_or_404)
from django.views.generic import (TemplateView, FormView, UpdateView, DetailView)
from django.views.generic.edit import FormMixin
from .models import CompanySettings
# from django.views.generic.edit import (UpdateView)
from .forms import CompanySettingsForm
from django.contrib import messages
from django.urls import reverse_lazy



class CompanySettingsView(FormMixin, DetailView):
    template_name = "site_settings/settings.html"
    form_class = CompanySettingsForm
    # success_url = reverse_lazy('site_settings:company-settings')
    success_url = reverse_lazy('company-settings')
    model = CompanySettings
    # Should match the value after ':' from url <slug:the_slug>
    # slug_url_kwarg = 'company'
    # Should match the name of the slug field on the model 
    # slug_field = 'slug' # DetailView's default value: optional
    # context_object_name = "object"

    def get_object(self):
        return get_object_or_404(CompanySettings, slug="company")


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # print(form.cleaned_data)
        print(form.cleaned_data.get("name"))
        return super().form_valid(form)



class AboutSettingsView(TemplateView):
    template_name = "site_settings/about.html"
