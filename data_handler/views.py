from django.views.generic import TemplateView, View
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db import transaction
from rest_framework.exceptions import ParseError
from rest_framework.parsers import (FileUploadParser, MultiPartParser, FormParser)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .helpers import *
import os, json, sys, traceback
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from .validators import CheckInDataError

DONOR_LBL = "Donation Field"
UNIQUE_ID_LBL = "Unique Identifier (ID)"


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
        data_file = DataFile.objects.get(member=request.user)
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

        ## save the file path after upload it into the db
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


class SaveColumnsView(APIView):
    """
    this view to save the selected columns with the data types and the unique id of the columns

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
        save_point = transaction.savepoint()
        all_columns_with_dtypes = []  # save all columns with data types which will save to db
        try:

            columns_name = request.POST.getlist(
                "columns[]")  # to save columns as text in db, [] -> this because the key send "columns[]"
            columns_name_dtypes = request.POST.get("columns_with_datatype")  # to save columns with the data types
            columns_name_dtypes_json = json.loads(columns_name_dtypes)

            if len(columns_name):
                columns_name = reorder_columns(columns_name_dtypes_json, True)
                # columns_names = "|".join(columns_name)
                # save the columns name only
                member_data_file.selected_columns = "|".join(columns_name)
                # double check if the unique id not in the columns that send from the client side
                if UNIQUE_ID_LBL.lower() not in columns_name_dtypes_json.values():
                    raise CheckInDataError("Unique ID Column not exists!!")

                # loop through columns name and the dtypes
                for col_name, col_dtype in columns_name_dtypes_json.items():
                    if col_dtype == UNIQUE_ID_LBL.lower():
                        member_data_file.unique_id_column = col_name

                    if col_dtype == DONOR_LBL.lower():
                        member_data_file.is_donor_id_selected = True

                    # save the column with data type in string
                    col_with_dtype = f"{col_name}:{col_dtype}"
                    all_columns_with_dtypes.append(col_with_dtype)

                reordered_columns = reorder_columns(all_columns_with_dtypes)
                # cprint(all_columns_with_dtypes, "green")
                member_data_file.selected_columns_dtypes = "|".join(reordered_columns)
                member_data_file.save()
                transaction.savepoint_commit(save_point)
                return Response("Extracted columns done, please wait to display the data..", status=200)
            else:
                return Response("No Columns Selected", status=401)

        except Exception as ex:
            transaction.savepoint_rollback(save_point)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            cprint(str(ex), "red")
            print(exc_type, fname, exc_tb.tb_lineno)
            print(traceback.format_exc())
            return Response(str(ex), status=401)

        finally:
            all_columns_with_dtypes = []  # to avoid any duplicate values or similar issues


class GetColumnsView(APIView):
    """
    API View to extract only columns name, to parse them to Datatable.js, then
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

        try:

            columns_list = member_data_file.get_selected_columns_with_dtypes

            # check if the member picked columns

            if len(columns_list) > 1:
                return Response(columns_list, status=200)
            else:
                delete_data_file(member_data_file.data_file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""
                member_data_file.selected_columns_dtypes = ""
                member_data_file.donor_id_column = ""
                member_data_file.is_donor_id_selected = False
                member_data_file.unique_id_column = ""
                return Response('', status=200)

        except (AttributeError, TypeError):
            return Response("No Data file uploaded Yet!", status=200)


class GetAllColumnsView(APIView):
    """
    API View to extract only columns name, to parse them to Datatable.js, then
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

        try:
            data_file_path = member_data_file.data_file_path
            all_columns = extract_columns_names(data_file_path)

            columns_list = member_data_file.get_selected_columns_with_dtypes

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
        from data_handler.models import DataFile
        member_data_file = DataFile.objects.get(member=request.user)
        try:
            # print(request.user)
            records_count = request.POST.get("recordsCount")
            file_path = member_data_file.data_file_path
            file_columns = member_data_file.get_selected_columns_as_list
            columns_with_dtypes = member_data_file.get_selected_columns_with_dtypes
            unique_column = member_data_file.unique_id_column

            # check if there is no columns picked from the user, delete and reupload the data file
            if len(file_columns) > 1:
                row_count = member_data_file.allowed_records_count
                data_file_rows = get_rows_data_by_columns(file_path, file_columns, records_count, columns_with_dtypes,
                                                          unique_column)
                return Response({"data": data_file_rows}, status=200, content_type='application/json')
            else:
                delete_data_file(file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""
                member_data_file.selected_columns_dtypes = ""
                member_data_file.donor_id_column = ""
                member_data_file.is_donor_id_selected = False
                member_data_file.unique_id_column = ""
                return Response("No Data file uploaded Yet!", status=200)

        except Exception as ex:
            cprint(str(ex), "red")
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
            columns_with_dtypes = member_data_file.get_selected_columns_with_dtypes
            # check if there is no columns picked from the user, delete and reupload the data file
            if len(file_columns) > 1:
                row_count = member_data_file.allowed_records_count
                data_file_rows = get_rows_data_by_search_query(file_path, file_columns, search_query,
                                                               columns_with_dtypes)
                return Response({"data": data_file_rows}, status=200, content_type='application/json')
            else:
                delete_data_file(file_path)
                member_data_file.data_file_path = "None"
                member_data_file.file_upload_procedure = "None"
                member_data_file.all_records_count = 0
                member_data_file.selected_columns = ""
                member_data_file.selected_columns_dtypes = ""
                member_data_file.donor_id_column = ""
                member_data_file.is_donor_id_selected = False
                member_data_file.unique_id_column = ""

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
                member_data_file.selected_columns_dtypes = ""
                member_data_file.donor_id_column = ""
                member_data_file.is_donor_id_selected = False
                member_data_file.unique_id_column = ""


        except Exception as ex:
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
            columns_with_dtypes = member_data_file.get_selected_columns_with_dtypes
            updated_rows = request.POST.get("rows")
            # print(updated_rows)
            json_data = json.loads(updated_rows)
            # print(len(json_data))
            only_used_rows_data = {}
            for key, value in json_data.items():
                if len(value) > 0:  # check and get the updated rows only
                    only_used_rows_data[key] = value
                    for single in value:
                        tmp_dtype = columns_with_dtypes[single['colName']]
                        # print(type(single['colValue']))
                        validate = validate_obj.detect_and_validate(single['colValue'], dtype=tmp_dtype)
                        # print(validate)

            column_names = member_data_file.get_selected_columns_as_list
            updated_data = update_rows_data(file_path, only_used_rows_data, column_names)
            # print(only_used_rows_data)
            response = ""
            if validate['is_error'] is False:
                response = Response({"is_error": False, "msg": updated_data}, status=200,
                                    content_type='application/json')
            else:
                response = Response({"is_error": True, "msg": updated_data}, status=200,
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
            member_data_file.selected_columns_dtypes = ""
            member_data_file.donor_id_column = ""
            member_data_file.is_donor_id_selected = False
            member_data_file.unique_id_column = ""
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
        columns = request.POST.get("columns")  # as a dict
        columns_json = json.loads(columns)  # as a dict
        print(columns_json)
        validate_columns_result = validate_data_type_in_dualbox(columns_json, data_file, columns_list)
        print(validate_columns_result)
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
            columns_with_dtypes = member_data_file.get_selected_columns_with_dtypes
            column_name = request.POST.get("column_name")
            clicked_row_count = request.POST.get("records_number")
            # clicked_row_count = 50
            all_validate_columns = get_not_validate_rows2(member_data_file.data_file_path, column_name,
                                                          member_data_file.get_selected_columns_as_list,
                                                          columns_with_dtypes, clicked_row_count)
            # return Response("Please wait while validate the date type...", status=200)
            print(all_validate_columns[0])
            return Response({"data": all_validate_columns}, status=200, content_type='application/json')


        except Exception as ex:
            cprint(str(ex), 'red')
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
            # {'is_accept_terms': True, 'is_accept_download_template': True, 'is_download_template': False}
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


class CheckMemberUpload(APIView):
    """
        ### Developement only ###
        API View to Check if member upload data file or not, to set the cookie

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        from data_handler.models import DataFile
        member_data_file = DataFile.objects.get(member=request.user)

        return Response(member_data_file.file_upload_procedure, status=200)
