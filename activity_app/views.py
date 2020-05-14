from django.shortcuts import render
from django.views.generic import TemplateView


class ListActivitiesView(TemplateView):
    template_name = "activity_app/list.html"
