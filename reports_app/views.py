from django.views.generic import TemplateView, View
from django.shortcuts import (reverse, redirect, render)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
import simplejson as simple_json
from urllib.parse import quote_plus
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db import connection
from faker import Faker
from prettyprinter import pprint
from termcolor import cprint
import random
import os, sys, traceback, json
from predict_me.my_logger import log_exception
from reports_app.helper import *
from users.models import Member
from django.http import JsonResponse

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
        generic_filters = ReportFilterGenerator.get_generic_filters()
        # custom_users_filters = ReportFilterGenerator.get_custom_filters('users')
        # generic_filters.extend(custom_users_filters)
        return render(request, "reports_app/list.html",
                      context={"dummy_data": faker_holder, 'title': "Users", "filter_columns": generic_filters})


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

        generic_filters = ReportFilterGenerator.get_generic_filters()
        custom_users_filters = ReportFilterGenerator.get_custom_filters('data_usage')
        generic_filters.extend(custom_users_filters)
        return render(request, "reports_app/list.html",
                      context={"dummy_data": faker_holder, 'title': "Data Usage", "filter_columns": generic_filters})


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
        import random
        cities_query = Member.objects.all().values_list('city', flat=False)
        all_cities = []
        for ci in cities_query:
            all_cities.append(ci[0])
        faker_obj = Faker()
        faker_holder = []
        tmp_item = []
        for _ in range(1, 25):
            amount = faker_obj.pyfloat(left_digits=None, right_digits=2, positive=False, min_value=200,
                                       max_value=600)
            addition_records = random.choice([200, 400, 600])
            amount_addition_records = 0.5 * addition_records
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "email": faker_obj.email(),
                "pay_date": faker_obj.date_this_year(),
                "sub_plan": faker_obj.word(SUB_PLANS),
                # "fee": random.choice([200, 400, 600]),
                'amount': amount,
                "addition_records": addition_records,
                "amount_addition_records": amount_addition_records,
                "total_amount": round(amount + amount_addition_records, 2)
            })

        generic_filters = ReportFilterGenerator.get_generic_filters()
        custom_users_filters = ReportFilterGenerator.get_custom_filters('revenue')
        generic_filters.extend(custom_users_filters)
        return render(request, "reports_app/list.html",
                      context={"dummy_data": faker_holder, 'title': "Revenue", "filter_columns": generic_filters,
                               "cities": all_cities})


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


class FetchReports(APIView):
    """
    API View to fetch required reports with its own filters and displayed columns
    and return the required data with columns

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def post(self, request, format=None):
        try:
            post_data = request.POST
            reports_section_name = request.POST.get("reports_section_name")
            all_filter_cookies = request.POST.get("all_filter_cookies")
            all_filter_cookies = json.loads(all_filter_cookies)
            displayed_columns = request.POST.get("displayed_columns")
            displayed_columns = json.loads(displayed_columns)
            cprint(reports_section_name, 'red')
            cprint(all_filter_cookies, 'yellow')
            cprint(len(all_filter_cookies), 'green')
            cprint(displayed_columns, 'blue')
            report_obj = ReportGenerator(reports_section_name, displayed_columns, all_filter_cookies)
            cprint(report_obj, 'magenta')

            return Response(
                {"table_header": report_obj.get_displayed_columns(), 'report_rows': report_obj.get_rows_file()},
                status=200)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())


class FilterReports(APIView):
    """
    API View to fetch required reports with its own filters and displayed columns
    and return the required data with columns

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def post(self, request, format=None):
        try:
            post_data = request.POST
            # cprint(request.POST, "blue")
            filter_array = json.loads(request.POST.get("filtersArray"))
            filter_report_section = request.POST.get("reportSectionName")
            # cprint(filter_array, "yellow")
            # cprint(filter_report_section, "red")
            reports_headers = ReportGenerator.generate_reports_table_header(filter_array)
            # cprint(reports_headers, "green")
            reports = ReportGenerator.generate_report(filter_report_section, filter_array, reports_headers,
                                                      request.user.pk)
            # ReportGenerator.generate_reports(filter_array)
            # cprint(reports.keys(), 'green')
            # cprint(simple_json.dumps(reports.get("data")), 'green')
            # cprint(json.dumps(reports.get("data")), 'green')
            # cprint(type(reports.get("data")), 'cyan')
            # cprint(reports, 'blue')
            # cprint(reports_headers, 'red')
            # cprint(reports.get("data"), 'blue')
            return Response(
                {"table_header": reports_headers, "report_data": reports.get('data'),
                 "report_section_name": filter_report_section},
                status=200)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())


class FetchReportData(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def post(self, request, *args, **kwargs):
        cities_query = Member.objects.all().values_list(request.POST.get("columnName"), flat=False)
        rows = []
        for ci in cities_query:
            rows.append(ci[0])

        return JsonResponse({"data": rows}, status=200)
