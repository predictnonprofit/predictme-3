from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from users.models import Member
from django.shortcuts import render, redirect, reverse
from ipware import get_client_ip


class ProfileOverview(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/overview.html", context={"member": member})


class ProfilePersonal(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/personal.html", context={"member": member})


class ProfileInformation(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/information.html", context={"member": member})


class ProfileChangePassword(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/change-password.html", context={"member": member})


class ProfileEmail(LoginRequiredMixin, View):
    # template_name = "members_app/profile/email.html"
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/email.html", context={"member": member})


class SubscriptionManageView(LoginRequiredMixin, View):
    # template_name = "members_app/profile/subscription.html"
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/subscription.html", context={"member": member})
