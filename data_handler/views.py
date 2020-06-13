from django.views.generic import TemplateView, View
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.exceptions import ParseError
from rest_framework.parsers import (FileUploadParser, MultiPartParser, FormParser)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .helpers import *
import os, json
from membership.models import UserMembership
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers


def data_handler_test_dual(request):
    return render(request, "data_handler/test/dual-box.html")


class DataListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    # template_name = "data_handler/list.html"
    def get(self, request, *args, **kwargs):
        return render(request, "data_handler/list.html")


@api_view(['POST'])
def data_handler_init(request):
    if request.method == "POST":
        picked_columns = request.POST.get("columns")
        return Response(request.POST)


def download_instructions_template(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "files", 'Donor File Template.xlsx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


class DataHandlerFileUpload(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, filename, format=None):
        from data_handler.models import DataFile
        from membership.models import UserMembership
        data_file = DataFile.objects.get(member=request.user)
        u_membership = UserMembership.objects.get(member=request.user)
        dfile = request.FILES['donor_file']

        path = default_storage.save(f"data/{dfile.name}", ContentFile(dfile.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        thefile = default_storage.open(path)
        row_count = get_row_count(tmp_file)  # get total rows of the uploaded file
        columns = extract_columns_names(tmp_file)  # extract the columns from the uploaded file
        print(columns)
        donor_id_names = {"id", "donor_id", "did", "donor_unique_identifier", "donor", 'donorid'}
        # check if the file columns have donor id column
        is_column_exists = False  # if true means the donor id column exists in the file
        for col in columns:
            if col.lower() in donor_id_names:
                is_column_exists = True
            else:
                is_column_exists = False
        ## save the file path after upload it into the db
        # if is_column_exists is True:
        if is_column_exists is False:
            if data_file.data_file_path is not None:
                data_file.data_file_path = tmp_file
                data_file.file_upload_procedure = "local_file"
                data_file.all_records_count = row_count
                data_file.save()
            if row_count > data_file.allowed_records_count:
                # return Response("Columns count bigger than the allowed")
                resp = {"is_allowed": False, "row_count": row_count}
                return Response(resp, status=200)
            else:
                resp = {"is_allowed": True, "columns": columns, "row_count": row_count}
                # print(columns)
                return Response(resp, status=200)
        else:
            resp = {"is_allowed": False, "columns": columns, "row_count": 0,
                    "msg": "The Donor ID column no exists, please read the upload instructions very carefully"}
            # print(columns)
            delete_data_file(tmp_file)
            return Response(resp, status=200)


class SaveColumnsView(APIView):
    """
    this view to save the selected views to db

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        from membership.models import UserMembership
        from data_handler.models import DataFile
        member_data_file = DataFile.objects.get(member=request.user)
        columns_names = request.POST.getlist("columns[]")  # to save columns as text in db
        print(columns_names)
        if len(columns_names):
            columns_names = "|".join(columns_names)
            member_data_file.selected_columns = columns_names
            member_data_file.save()
            return Response("Extracted columns done, please wait to display the data..", status=200)
        else:
            return Response("No Columns Selected", status=401)


class GetColumnsView(APIView):
    """
    API View to extract only columns namee, to parse them to Datatable.js, then
    datatable.js request to another apiview to get the rows

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        from data_handler.models import DataFile
        member_data_file = DataFile.objects.get(member=request.user)
        data = request.POST
        try:
            columns_list = member_data_file.get_selected_columns_as_list

            return Response(columns_list, status=200)
        except AttributeError:
            return Response("No Data file uploaded Yet!", status=200)


class GetAllColumnsView(APIView):
    """
    API View to extract only columns namee, to parse them to Datatable.js, then
    datatable.js request to another apiview to get the rows

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        from data_handler.models import DataFile
        member_data_file = DataFile.objects.get(member=request.user)
        data = request.POST
        try:
            data_file_path = member_data_file.data_file_path
            all_columns = extract_columns_names(data_file_path)
            columns_list = member_data_file.get_selected_columns_as_list
            print(all_columns)

            return Response(all_columns, status=200)
        except AttributeError:
            return Response("No Data file uploaded Yet!", status=200)


class GetRowsView(APIView):
    """
    API View to get all rows from member data file, to Datatable.js ajax request to bring 
    the data from the member uploaded file

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        try:
            # print(request.user)
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            file_path = member_data_file.data_file_path
            file_columns = member_data_file.get_selected_columns_as_list
            row_count = member_data_file.allowed_records_count
            data_file_rows = get_rows_data_by_columns(file_path, file_columns, row_count)
            data_file_rows_json = json.dumps(data_file_rows)
            # return JsonResponse({"data": data_file_rows})
            # return Response(data_file_rows_json, status=200, content_type='application/json')
            return Response({"data": data_file_rows}, status=200, content_type='application/json')


        except AttributeError:
            return Response("No Data file uploaded Yet!", status=200)


class SaveNewRowsUpdateView(APIView):
    """
    API View to save all updated rows from data table form, 

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        try:
            # print(request.user)
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            file_path = member_data_file.data_file_path
            # print(file_path)
            print(request.POST)
            import json
            # rows = json.loads(request.POST)
            # for key, value in request.POST.items():
            #     print(key, " --> ", value)

            return Response("Get the rows", status=200)


        except AttributeError:
            return Response("No Data file uploaded Yet!", status=200)


class DeleteDataFileView(APIView):
    """
    ### Developement only ###
    API View to save all updated rows from data table form, 

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        try:
            # print(request.user)
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            delete_data_file(member_data_file.data_file_path)
            member_data_file.data_file_path = "None"
            member_data_file.file_upload_procedure = "None"
            member_data_file.all_records_count = 0
            member_data_file.selected_columns = ""
            member_data_file.save()

            return Response("File Delete Successfully", status=200)


        except Exception as ex:
            print(ex)
            return Response(str(ex), status=200)


class ValidateColumnsView(APIView):
    """
    ### Developement only ###
    API View to validate columns data type, 

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = (IsAuthenticated,)

    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        try:
            # print(request.user)
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            columns = request.POST.get("columns")
            # print(type(columns))
            columns_json = json.loads(columns)
            print(columns_json)
            if len(columns_json) > 3:
                return Response("Please wait while validate the date type...", status=200)

            else:
                return Response("Please select at least 3 columns with the data type!", status=200)




        except Exception as ex:
            print(ex)
            return Response(str(ex), status=200)
