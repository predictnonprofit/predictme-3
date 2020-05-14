from django.views.generic import TemplateView


class UsersListView(TemplateView):
    template_name = "dash_users/list.html"


class UsersCreateView(TemplateView):
    template_name = "dash_users/create.html"


class UsersPendingView(TemplateView):
    template_name = "dash_users/list_pending.html"