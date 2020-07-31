from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from users.models import Member
from django.shortcuts import render, redirect, reverse
from data_handler.helpers import download_data_file_converter
from pathlib import Path
from termcolor import cprint
import os
import pandas as pd
from django.conf import settings
from datetime import date
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
import traceback
from predict_me.my_logger import (log_info, log_exception)


def download_instructions_template(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "files", 'Donor File Template.xlsx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


def download_data_file_xlsx(request):
    from data_handler.models import DataFile
    data_file = DataFile.objects.get(member=request.user)
    selected_columns = data_file.selected_columns.split("|")
    # download_data_file_converter(data_file)
    new_xlsx_path = None
    try:
        file_path = Path() / settings.MEDIA_ROOT / "data" / f'{data_file.data_file_path}'
        response = None

        # first check if the file is csv or xlsx file, to converted to csv file
        if file_path.suffix == ".csv":
            new_xlsx_path = file_path.parent / f"{os.path.splitext(file_path.name)[0]}.xlsx"
            # read_csv_file = pd.read_csv(file_path.as_posix())  # file with all columns
            read_csv_file = pd.read_csv(file_path.as_posix(), usecols=selected_columns,
                                        skipinitialspace=True)  # file with selected columns
            # read_csv_file[selected_columns].to_excel(new_xlsx_path, header=True, index=False)  # file with selected columns
            read_csv_file.to_excel(new_xlsx_path, header=True, index=False)
            # cprint('convert to xlsx', "yellow")
            with open(new_xlsx_path, 'rb') as fh:
                response = HttpResponse(fh.read(),
                                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response['Content-Disposition'] = 'inline; filename=' + f"PredictME_{date.today()}.xlsx"

        elif file_path.suffix == ".xlsx":
            with open(file_path.as_posix(), 'rb') as fh:
                response = HttpResponse(fh.read(),
                                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response['Content-Disposition'] = 'inline; filename=' + f"PredictME_{date.today()}.xlsx"

    except Exception as ex:
        cprint(str(ex), 'red')
    else:
        return response

    finally:
        if new_xlsx_path:
            new_xlsx_path.unlink()
            cprint("Deleting xlsx file...", 'red')


def download_data_file_csv(request):
    from data_handler.models import DataFile
    data_file = DataFile.objects.get(member=request.user)
    selected_columns = data_file.selected_columns.split("|")
    new_csv_path = None
    try:
        file_path = Path() / settings.MEDIA_ROOT / "data" / f'{data_file.data_file_path}'
        response = None
        # first check if the file is csv or xlsx file, to converted to csv file
        if file_path.suffix == ".xlsx":
            new_csv_path = file_path.parent / f"{os.path.splitext(file_path.name)[0]}.csv"
            # read_xlsx_file = pd.read_excel(file_path.as_posix())   # file with all columns
            read_xlsx_file = pd.read_excel(file_path.as_posix(), usecols=selected_columns)  # file with selected columns
            read_xlsx_file.to_csv(new_csv_path, header=True, index=False)
            # cprint('convert to csv', "yellow")
            with open(new_csv_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/csv")
                response['Content-Disposition'] = 'inline; filename=' + f"PredictME_{date.today()}.csv"

        elif file_path.suffix == ".csv":
            with open(file_path.as_posix(), 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/csv")
                response['Content-Disposition'] = 'inline; filename=' + f"PredictME_{date.today()}.csv"

    except Exception as ex:
        cprint(str(ex), 'red')

    else:
        return response

    finally:
        if new_csv_path:
            new_csv_path.unlink()
            cprint("Deleting csv file...", 'red')


def download_dashboard_pdf(request):
    try:
        from django.core.files.storage import FileSystemStorage
        request.build_absolute_uri('/')
        html_string = render_to_string('members_app/profile/dashboard.html')

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/dashboard.pdf');

        fs = FileSystemStorage('/tmp')
        with fs.open('dashboard.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="dashboard.pdf"'
            return response

    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        log_exception(traceback.format_exc())


class ProfileOverview(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/overview.html", context={"member": member})


class ProfileDashboard(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        member = Member.objects.get(email=request.user.email)
        return render(request, "members_app/profile/dashboard.html", context={"member": member})


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
