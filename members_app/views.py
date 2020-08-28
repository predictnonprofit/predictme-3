from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
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
from xhtml2pdf import pisa
from django.http import HttpResponse
import traceback
from predict_me.my_logger import (log_info, log_exception)
from django.contrib import messages

ANNUAL_REVENUE = (
    '$5,000 - $50,000', '$50,000 - $100,000',
    '$100,000 - $250,000', '$250,000 - $500,000',
    '$500,000 - $1 million', '$1 million - $5 million',
    '$5 million - $10 million', '$10 million or more'
)

ORGANIZATION_TYPES = (
    'Higher Education', 'Other Education', 'Health related',
    'Hospitals and Primary Care', 'Human and Social Services',
    'Environment', 'Animal', 'International', 'Religion related',
    'Other'
)


@login_required
def download_instructions_template(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "files", 'Donor File Template.xlsx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


@login_required
def download_data_file_xlsx(request, id):
    session_id = int(id)
    from data_handler.models import (DataFile, DataHandlerSession)
    data_file = DataFile.objects.get(member=request.user)
    member_data_session = DataHandlerSession.objects.get(data_handler_id=data_file, pk=session_id)
    selected_columns = member_data_session.selected_columns.split("|")
    # download_data_file_converter(data_file)
    new_xlsx_path = None
    try:
        file_path = Path() / settings.MEDIA_ROOT / "data" / f'{member_data_session.data_file_path}'
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
            import random
            new_tmp_xlsx_path = file_path.parent / f"{random.randint(0, 100)}_{os.path.splitext(file_path.name)[0]}.xlsx"
            read_tmp_xlsx_file = pd.read_excel(file_path.as_posix(),
                                               usecols=selected_columns)  # file with selected columns
            read_tmp_xlsx_file.to_excel(new_tmp_xlsx_path, header=True, index=False)
            with open(new_tmp_xlsx_path.as_posix(), 'rb') as fh:
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
        elif new_tmp_xlsx_path:
            new_tmp_xlsx_path.unlink()
            cprint("Deleting Temp xlsx file...", 'red')


@login_required
def download_data_file_csv(request, id):
    session_id = int(id)
    from data_handler.models import (DataFile, DataHandlerSession)
    data_file = DataFile.objects.get(member=request.user)
    member_data_session = DataHandlerSession.objects.get(data_handler_id=data_file, pk=session_id)
    selected_columns = member_data_session.selected_columns.split("|")
    new_csv_path = None
    try:
        file_path = Path() / settings.MEDIA_ROOT / "data" / f'{member_data_session.data_file_path}'
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
            import random
            new_tmp_csv_path = file_path.parent / f"{random.randint(0, 100)}_{os.path.splitext(file_path.name)[0]}.xlsx"
            read_tmp_csv_file = pd.read_csv(file_path.as_posix(), usecols=selected_columns,
                                            skipinitialspace=True)  # file with selected columns
            read_tmp_csv_file.to_csv(new_tmp_csv_path, header=True, index=False)
            with open(new_tmp_csv_path.as_posix(), 'rb') as fh:
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
        elif new_tmp_csv_path:
            new_tmp_csv_path.unlink()
            cprint("Deleting Tmp csv file...", 'red')


@login_required
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


class ProfilePersonal(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        # cprint(self.request.user, 'blue')
        return True

    def get(self, request):
        try:
            member = Member.objects.get(email=request.user.email)
            return render(request, "members_app/profile/personal.html", context={"member": member})
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())

    def post(self, request):
        try:
            member = Member.objects.get(email=request.user.email)
            member.first_name = request.POST.get("first-name").strip()
            member.last_name = request.POST.get("last-name").strip()
            member.full_name = f'{request.POST.get("first-name").strip()} {request.POST.get("last-name").strip()}'
            member.email = request.POST.get("email").strip()
            member.phone = request.POST.get("phone").strip()
            member.save()
            messages.success(request, 'your info have been updated successfully!')
            return redirect(reverse('profile-personal'))

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
            messages.error(request, 'There is errors!, try again latter')


class ProfileInformation(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        try:
            member = Member.objects.get(email=request.user.email)
            return render(request, "members_app/profile/information.html",
                          context={"member": member, 'annual_revenue': ANNUAL_REVENUE, 'org_types': ORGANIZATION_TYPES})
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())

    def post(self, request):
        try:
            member = Member.objects.get(email=request.user.email)
            # ['csrfmiddlewaretoken', 'org_name', 'org_website', 'organizationType', 'annualRevenue', 'job_title', 'total_staff', 'num_of_volunteer']
            member.org_name = request.POST.get("org_name").strip()
            member.org_website = request.POST.get("org_website").strip()
            if request.POST.get("org_type") != "Other":
                member.org_type = request.POST.get("org_type").strip()
            else:
                member.org_type = request.POST.get("other-org-type").strip()
            member.annual_revenue = request.POST.get("annualRevenue").strip()
            member.job_title = request.POST.get("job_title").strip()
            member.total_staff = request.POST.get("total_staff").strip()
            member.num_of_volunteer = request.POST.get("num_of_volunteer").strip()
            member.num_of_board_members = request.POST.get("num_of_board_members").strip()
            member.save()

            messages.success(request, 'your info have been updated successfully!')
            return redirect(reverse('profile-info'))

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
            messages.error(request, 'There is errors!, try again latter')


class ProfileChangePassword(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        try:
            member = Member.objects.get(email=request.user.email)
            return render(request, "members_app/profile/change-password.html", context={"member": member})
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())

    def post(self, request):
        try:
            # ^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$
            import re
            member = Member.objects.get(email=request.user.email)
            # 'password', 'new-password', 'verify-new-password'
            if request.POST.get('password') == '':
                messages.error(request, 'Password is empty!!')
            elif request.POST.get("new-password") == "":
                messages.error(request, 'New Password is empty!!')
            elif request.POST.get("verify-new-password") == "":
                messages.error(request, 'You have to verify new password is empty!!')
            elif request.POST.get("verify-new-password") != request.POST.get("new-password"):
                messages.error(request, 'Password not verified or matched!!')
            else:
                if member.check_password(request.POST.get("password")) is True:

                    pattern = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")
                    if pattern.match(request.POST.get('new-password')):
                        member.set_password(request.POST.get("new-password"))
                        member.save()
                        update_session_auth_hash(request, member)
                        messages.success(request, 'Your password has been updated!')
                    else:
                        messages.error(request, 'Your password not match password requirements!')

                else:
                    messages.error(request, 'Your old password is not correct!')
            return redirect(reverse('profile-change-password'))

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
            messages.error(request, 'There is errors!, try again latter')


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
