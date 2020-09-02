from django.views.generic import TemplateView, View
from django.shortcuts import (reverse, redirect, render)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from urllib.parse import quote_plus
from faker import Faker
from prettyprinter import pprint
from termcolor import cprint
import random

USERS_STATUS = ("Active", 'Pending', 'Cancel')
SUB_PLANS = ("Starter", 'Professional', 'Expert')


class ReportsListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        return render(request, "reports_app/list.html")


class ReportsUsersListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        cprint("list reports", 'yellow')
        faker_obj = Faker()
        faker_holder = []
        for _ in range(1, 20):
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "email": faker_obj.email(),
                "reg_date": faker_obj.date_this_year(),
                "status": faker_obj.word(USERS_STATUS),
                "sub_plan": faker_obj.word(SUB_PLANS),
            })

        return render(request, "reports_app/list.html", context={"dummy_data": faker_holder, 'title': "Users"})


class ReportsDataUsageView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        cprint("list reports", 'yellow')
        faker_obj = Faker()
        faker_holder = []
        for _ in range(1, 25):
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "email": faker_obj.email(),
                "last_run": faker_obj.date_this_year(),
                "total_rec_used": faker_obj.random_int(0, 600),
                "sub_plan": faker_obj.word(SUB_PLANS),
                "usage": faker_obj.random_int(0, 100),
            })

        return render(request, "reports_app/list.html",
                      context={"dummy_data": faker_holder, 'title': "Data Records Using"})



class ReportsExtraUsageView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        cprint("list reports", 'yellow')
        faker_obj = Faker()
        faker_holder = []
        tmp_item = []
        for _ in range(1, 25):
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "email": faker_obj.email(),
                "last_run": faker_obj.date_this_year(),
                "total_rec_used": faker_obj.random_int(0, 600),
                "sub_plan": faker_obj.word(SUB_PLANS),
                "money": faker_obj.pyfloat(left_digits=None, right_digits=2, positive=False, min_value=10,
                                           max_value=1500),
            })

        return render(request, "reports_app/list.html", context={"dummy_data": faker_holder, 'title': 'Extra Records'})


class ReportsRevenuesView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        faker_obj = Faker()
        faker_holder = []
        tmp_item = []
        for _ in range(1, 25):
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "pay_date": faker_obj.date_this_year(),
                "sub_plan": faker_obj.word(SUB_PLANS),
                # "fee": random.choice([200, 400, 600]),
                'fee': faker_obj.pyfloat(left_digits=None, right_digits=2, positive=False, min_value=10,
                                         max_value=1500),
                'product': faker_obj.word(("Extra Records", 'Renewal Fee')),
            })

        return render(request, "reports_app/list.html",
                      context={"dummy_data": faker_holder, 'title': 'Revenues reports'})


class ProfitShareView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        faker_obj = Faker()
        faker_holder = []
        for _ in range(1, 25):
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "pay_date": faker_obj.date_this_year(),
                "email": faker_obj.email(),
                "sub_plan": faker_obj.word(SUB_PLANS),
                # "fee": random.choice([200, 400, 600]),
                # 'fee': faker_obj.pyfloat(left_digits=None, right_digits=2, positive=False, min_value=10,
                #                          max_value=1500),
                "fee": faker_obj.random_int(0, 200),
                'product': faker_obj.word(("Extra Records", 'Renewal Fee')),
            })

        return render(request, "reports_app/list.html",
                      context={"dummy_data": faker_holder, 'title': 'Profit Share'})
