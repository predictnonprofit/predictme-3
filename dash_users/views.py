from django.views.generic import TemplateView
from django.shortcuts import (redirect, reverse)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)



class UsersListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dash_users/list.html"

    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))


class UsersCreateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dash_users/create.html"
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))


class UsersDetailsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dash_users/details.html"
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))


class UsersPendingView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dash_users/list_pending.html"
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))