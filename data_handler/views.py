from django.views.generic import TemplateView


class DataListView(TemplateView):
    template_name = "data_handler/list.html"