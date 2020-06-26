from django.views.generic import TemplateView, View
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
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
        save_data_file_rounded(tmp_file)
        thefile = default_storage.open(path)
        row_count = get_row_count(tmp_file)  # get total rows of the uploaded file
        columns = extract_columns_names(tmp_file)  # extract the columns from the uploaded file
        # print(columns)
        donor_id_names = {"id", "donor_id", "did", "donor_unique_identifier", "donor", 'donorid', "unique Code",
                          "unique_code", "donor id"}
        # check if the file columns have donor id column
        is_column_exists = False  # if true means the donor id column exists in the file
        for col in columns:
            # print(col.lower() in donor_id_names)
            if col.lower() in donor_id_names:
                is_column_exists = True
                break
            else:
                is_column_exists = False
        ## save the file path after upload it into the db
        if is_column_exists is True:
            # if is_column_exists is False:
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
            # check if the member picked columns

            if len(columns_list) > 1:
                return Response(columns_list, status=200)
            else:
                delete_data_file(member_data_file.data_file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""
                return Response('', status=200)

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
            # print(all_columns)

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
            records_count = request.POST.get("recordsCount")
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            file_path = member_data_file.data_file_path
            file_columns = member_data_file.get_selected_columns_as_list
            # check if there is no columns picked from the user, delete and reupload the data file
            if len(file_columns) > 1:
                row_count = member_data_file.allowed_records_count
                data_file_rows = get_rows_data_by_columns(file_path, file_columns, records_count)
                return Response({"data": data_file_rows}, status=200, content_type='application/json')
            else:
                delete_data_file(file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""

        except AttributeError:
            return Response("No Data file uploaded Yet!", status=200)


class GetRowsBySearchQueryView(APIView):
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
            search_query = request.POST.get("searchQuery")
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            file_path = member_data_file.data_file_path
            file_columns = member_data_file.get_selected_columns_as_list
            # check if there is no columns picked from the user, delete and reupload the data file
            if len(file_columns) > 1:
                row_count = member_data_file.allowed_records_count
                data_file_rows = get_rows_data_by_search_query(file_path, file_columns, search_query)
                return Response({"data": data_file_rows}, status=200, content_type='application/json')
            else:
                delete_data_file(file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""

        except AttributeError:
            return Response("No Data file uploaded Yet!", status=200)


class NotValidateRowsView(APIView):
    """
    API View to get rows with not validate data, by column name
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
            col_name = request.POST.get("column_name")
            # print(request.POST)
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            file_path = member_data_file.data_file_path
            file_columns = member_data_file.get_selected_columns_as_list
            # check if there is no columns picked from the user, delete and re-upload the data file
            if len(file_columns) > 1:
                row_count = member_data_file.allowed_records_count
                data_file_rows = get_not_validate_rows(file_path, file_columns, col_name)
                data_file_rows_json = json.dumps(data_file_rows)
                return Response({"data": data_file_rows}, status=200, content_type='application/json')
            else:
                delete_data_file(file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""

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
            from .validators import DataValidator
            validate_obj = DataValidator()
            # print(request.user)
            from data_handler.models import DataFile
            member_data_file = DataFile.objects.get(member=request.user)
            file_path = member_data_file.data_file_path
            # print(file_path)
            import json
            updated_rows = request.POST.get("rows")
            # print(updated_rows)
            json_data = json.loads(updated_rows)
            # print(len(json_data))
            only_used_rows_data = {}
            for key, value in json_data.items():
                if len(value) > 0:  # check and get the updated rows only
                    only_used_rows_data[key] = value
                    for single in value:
                        validate = validate_obj.detect_and_validate(single['colValue'])

            column_names = member_data_file.get_selected_columns_as_list
            updated_data = update_rows_data(file_path, only_used_rows_data, column_names)
            # print(only_used_rows_data)
            response = ""
            if validate['is_error'] is False:
                response = Response({"is_error": False, "msg": "Data Saved"}, status=200,
                                    content_type='application/json')
            else:
                response = Response({"is_error": True, "msg": "Data Saved, but the data not valid"}, status=200,
                                    content_type='application/json')
            return response


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
        # try:
        # print(request.user)
        from data_handler.models import DataFile
        member_data_file = DataFile.objects.get(member=request.user)
        data_file = member_data_file.data_file_path
        columns_list = member_data_file.get_selected_columns_as_list
        columns = request.POST.get("columns")
        #             print(type(columns))  # as a string
        columns_json = json.loads(columns)  # as a dict
        validate_columns_result = validate_data_type_in_dualbox(columns_json, data_file, columns_list)
        if len(columns_json) > 3:
            return Response({"msg": "THe message is here"}, status=200, content_type='application/json')

        else:
            return Response("Please select at least 3 columns with the data type!", status=200)

    # except Exception as ex:
    #     print(ex)
    #     return Response(str(ex), status=200)


class FilterRowsView(APIView):
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
            column_name = request.POST.get("column_name")
            clicked_row_count = request.POST.get("records_number")
            # clicked_row_count = 50
            all_validate_columns = get_not_validate_rows2(member_data_file.data_file_path, column_name,
                                                          member_data_file.get_selected_columns_as_list,
                                                          clicked_row_count)
            # return Response("Please wait while validate the date type...", status=200)
            return Response({"data": all_validate_columns}, status=200, content_type='application/json')


        except Exception as ex:
            print(ex)
            return Response(str(ex), status=200)


class AcceptsDownload(APIView):
    """
        ### Developement only ###
        API View to save the member accepts and download counter

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            #{'is_accept_terms': True, 'is_accept_download_template': True, 'is_download_template': False}
            download_data = json.loads(request.POST.get("accept_data"))
            from data_handler.models import MemberDownloadCounter
            member_down_counter = MemberDownloadCounter.objects.get(member=request.user)
            member_down_counter.download_counter += 1
            member_down_counter.is_download_template = download_data['is_download_template']
            member_down_counter.save()
            return Response("update done", status=200)

        except ObjectDoesNotExist:
            # if the member not exists before
            new_rec = MemberDownloadCounter()
            new_rec.member = request.user
            new_rec.download_counter = 1
            new_rec.is_accept_terms = download_data['is_accept_terms']
            new_rec.is_accept_download_template = download_data['is_accept_download_template']
            new_rec.is_download_template = download_data['is_download_template']
            new_rec.save()
            return Response("save done", status=200)

        except Exception as ex:
            print(ex)
            return Response(str(ex), status=200)
