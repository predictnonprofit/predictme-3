from django.views.generic import TemplateView, View
from django.shortcuts import (reverse, redirect, render)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from urllib.parse import quote_plus
from faker import Faker
from prettyprinter import pprint

USERS_STATUS = ("Active", 'Pending', 'Cancel')


class ReportsListView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request, *args, **kwargs):
        filter_type = request.GET.get("reports", "")
        if filter_type != "":
            print(filter_type)
        if filter_type == "users":
            faker_obj = Faker()
            faker_holder = []
            tmp_item = []
            for _ in range(1, 20):
                faker_holder.append({
                    "id": _,
                    "name": faker_obj.name(),
                    "email": faker_obj.email(),
                    "reg_date": faker_obj.date_this_year(),
                    "status": faker_obj.word(USERS_STATUS),
                })

            return render(request, "reports_app/list.html", context={"dummy_data": faker_holder})

        return render(request, "reports_app/list.html")
