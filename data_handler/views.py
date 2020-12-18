from django.views.generic import (TemplateView, View, DetailView)
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
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
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from rest_framework.permissions import IsAuthenticated
from .validators import CheckInDataError
from django.contrib.auth.decorators import login_required
from prettyprinter import pprint
from django.core.signing import Signer
from django.http import (HttpResponse, Http404)
from django.utils.encoding import smart_str
import uuid
DONOR_LBL = "Donation Field"
UNIQUE_ID_LBL = "Unique Identifier (ID)"


def data_handler_test_dual(request):
    return render(request, "data_handler/test/dual-box.html")


class SessionDetailsView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy("login")

    def test_func(self):
        try:
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=self.request.user)
            session_id = self.kwargs.get('id')
            member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file, pk=session_id)
            if self.request.user == member_data_session.data_handler_id.member:
                return True
            return False
        except DataHandlerSession.DoesNotExist:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
            return False

    def get(self, request, *args, **kwargs):
        try:
            session_id = int(kwargs.get('id', None))
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            member_data_session = DataHandlerSession.objects.filter(data_handler_id=member_data_file,
                                                                    pk=session_id).first()

            return render(request, "data_handler/details.html", context={"session_info": member_data_session})

        except DataHandlerSession.DoesNotExist:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
            return redirect(reverse("data-handler-default"))


def session_details(request, id):
    # cprint(id, 'blue')
    return render(request, "data_handler/details.html")


class DataListView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    # template_name = "data_handler/list.html"
    def get(self, request, *args, **kwargs):
        try:
            context = {}
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            # member_data_session = DataHandlerSession.objects.filter(data_handler_id=member_data_file).count()
            member_data_session = DataHandlerSession.objects.filter(data_handler_id=member_data_file)
            context['member_sessions'] = member_data_session
            if member_data_file.data_sessions_set.count() > 0:
                context['has_session'] = True
                context['is_process_complete'] = member_data_session.first().is_process_complete
            else:
                context['has_session'] = False
                context['is_process_complete'] = False



            # this step will work when the member upload the file but did not pick any column
            # file_path = member_data_file.data_file_path
            # file_columns = member_data_file.get_selected_columns_as_list
            # columns_with_dtypes = member_data_file.get_selected_columns_with_dtypes
            # unique_column = member_data_file.unique_id_column
            # if (not bool(unique_column) and not bool(columns_with_dtypes)) and file_path != "None":
            #     delete_data_file(member_data_file.data_file_path)
            #     delete_all_member_data_file_info(member_data_file)
            # cprint(context, 'blue')
            # cprint(dir(request.user), "blue")
            # pprint(dir(request.user))
            return render(request, "data_handler/list.html", context=context)



        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())


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
        try:
            from data_handler.models import (DataFile, DataHandlerSession)
            data_file = DataFile.objects.get(member=request.user)
            dfile = request.FILES['donor_file']
            base_file_content = ContentFile(dfile.read())
            # this to make file name unique
            file_id = uuid.uuid4()
            new_file_name_id = f"{file_id.time_hi_version}-{dfile.name}"

            path = default_storage.save(f"data/{new_file_name_id}", base_file_content)
            # this step to save the base path with the old data type without convert the dtypes of the columns
            unique_user_data_file_ids = f"{str(data_file.id)}_{str(data_file.member.id)}"
            signer = Signer(algorithm='md5')
            base_path_name = f"{unique_user_data_file_ids}_{uuid.uuid4().hex[:6].upper()}_{dfile.name}"
            base_path = default_storage.save(f"data/base/{base_path_name}", base_file_content)
            tmp_base_path = os.path.join(settings.MEDIA_ROOT, base_path)
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            row_count = get_row_count(tmp_file)  # get total rows of the uploaded file

            # first check if the file empty or not
            if check_empty_df(tmp_file) is True:
                resp = {"is_allowed": False, "row_count": row_count,
                        "msg": "The file is empty please re-upload correct file", "is_empty": True}
                delete_data_file(tmp_file)
                delete_data_file(tmp_base_path)
                # delete_all_member_data_file_info(data_file)
                return Response(resp, status=200)
            else:
                # here the file not empty
                save_data_file_rounded(tmp_file)
                remove_spaces_from_columns_names(tmp_base_path)
                columns = extract_all_columns_with_dtypes(tmp_file)  # extract the columns from the uploaded file
                params = request.POST.get('parameters')
                session_label = request.POST.get('session-label')
                file_name = request.POST.get('file_name')
                data_or_num = check_data_or_num(params)
                if isinstance(data_or_num, int) is True:
                    member_data_session = DataHandlerSession.objects.get(data_handler_id=data_file,
                                                                         pk=data_or_num)
                    member_data_session.data_file_path = tmp_file
                    member_data_session.base_data_file_path = tmp_base_path
                    member_data_session.file_name = file_name
                    member_data_session.data_handler_session_label = session_label
                    member_data_session.save()
                else:
                    all_main_columns_dtypes = extract_all_columns_with_dtypes(tmp_file)
                    all_main_cols_str = ""
                    for key, value in all_main_columns_dtypes.items():
                        all_main_cols_str += f"{key}:{value}|"
                    member_data_session = DataHandlerSession.objects.create(data_handler_id=data_file,
                                                                            data_file_path=tmp_file,
                                                                            file_upload_procedure="local_file",
                                                                            all_records_count=row_count,
                                                                            data_handler_session_label=session_label,
                                                                            file_name=file_name,
                                                                            all_columns_with_dtypes=all_main_cols_str,
                                                                            base_data_file_path=tmp_base_path)
                    data_file.last_uploaded_session = member_data_session.pk
                    data_file.save()

                # cprint(member_data_session.pk, 'yellow')
                # check if the member has previous session before

                # save the file path after upload it into the db

                if row_count > data_file.allowed_records_count:
                    # return Response("Columns count bigger than the allowed")
                    resp = {"is_allowed": False, "row_count": row_count}
                    return Response(resp, status=200)
                else:
                    resp = {"is_allowed": True, "columns": columns, "row_count": row_count}
                    # print(columns)
                    return Response(resp, status=200)


        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())


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

    def post(self, request, *args, **kwargs):
        # save_point = transaction.savepoint()
        all_columns_with_dtypes = []  # save all columns with data types which will save to db
        try:
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)

            columns_name = request.POST.getlist(
                "columns[]")  # to save columns as text in db, [] -> this because the key send "columns[]"
            columns_name_dtypes = request.POST.get("columns_with_datatype")  # to save columns with the data types
            columns_name_dtypes_json = json.loads(columns_name_dtypes)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
            else:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=member_data_file.last_uploaded_session)

            if len(columns_name):
                columns_name = reorder_columns(columns_name_dtypes_json, True)
                # columns_names = "|".join(columns_name)
                # save the columns name only
                member_data_session.selected_columns = "|".join(columns_name)
                # double check if the unique id not in the columns that send from the client side
                if UNIQUE_ID_LBL.lower() not in columns_name_dtypes_json.values():
                    raise CheckInDataError("Unique ID Column not exists!!")

                # loop through columns name and the dtypes
                for col_name, col_dtype in columns_name_dtypes_json.items():
                    if col_dtype == UNIQUE_ID_LBL.lower():
                        member_data_session.unique_id_column = col_name

                    if col_dtype == DONOR_LBL.lower():
                        member_data_session.is_donor_id_selected = True

                    # save the column with data type in string
                    col_with_dtype = f"{col_name}:{col_dtype}"
                    all_columns_with_dtypes.append(col_with_dtype)
                reordered_columns = reorder_columns(all_columns_with_dtypes)
                member_data_session.selected_columns_dtypes = "|".join(reordered_columns)
                member_data_session.save()
                # transaction.savepoint_commit(save_point)
                return Response("Extracted columns done, please wait to display the data..", status=200)
            else:
                return Response("No Columns Selected", status=401)

        except Exception as ex:
            # transaction.savepoint_rollback(save_point)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # cprint(str(ex), "red")
            # print(exc_type, fname, exc_tb.tb_lineno)
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
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

        try:
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
                columns_list = member_data_session.get_selected_columns_with_dtypes
                # check if the member picked columns
                if len(columns_list) > 1:
                    return Response(columns_list, status=200)
                else:
                    # delete_data_file(member_data_session.data_file_path)
                    # delete_all_member_data_file_info(member_data_session)
                    return Response('No Columns', status=201)
            else:
                return Response("Not Integer number Passed!!", status=200)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
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
        from data_handler.models import (DataFile, DataHandlerSession)
        member_data_file = DataFile.objects.get(member=request.user)

        try:
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
                data_file_path = member_data_session.data_file_path
                # all_columns = extract_all_columns_with_dtypes(data_file_path)
                all_columns = member_data_session.get_all_data_file_columns
                selected_columns = member_data_session.get_selected_columns_with_dtypes
                unique_column = member_data_session.unique_id_column
                return Response(
                    {"all_columns": all_columns, "selected_columns": selected_columns, "unique_column": unique_column},
                    status=200, content_type='application/json')
        except AttributeError as aerr:
            log_exception(traceback.format_exc())
            return Response("No Data file uploaded Yet!", status=200)
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())


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
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
                # print(request.user)
                records_count = request.POST.get("recordsCount")
                file_path = member_data_session.data_file_path
                file_columns = member_data_session.get_selected_columns_as_list
                columns_with_dtypes = member_data_session.get_selected_columns_with_dtypes
                unique_column = member_data_session.unique_id_column
                all_original_columns = member_data_session.get_all_data_file_columns
                # check if there is no columns picked from the user, delete and re-upload the data file
                if len(file_columns) > 1:
                    row_count = member_data_file.allowed_records_count
                    data_file_rows = get_rows_data_by_columns(file_path, file_columns, records_count,
                                                              columns_with_dtypes,
                                                              all_original_columns)
                    # pprint(data_file_rows[0])
                    return Response({"data": data_file_rows, "total_rows": len(data_file_rows)}, status=200,
                                    content_type='application/json')
                    # return Response('{"data": ''}', content_type='application/json')
                else:
                    delete_data_file(file_path)
                    delete_all_member_data_file_info(member_data_session)
                    return Response("All of the data has been delete!", status=204)
            else:
                return Response("", status=200)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
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
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
                file_path = member_data_session.data_file_path
                file_columns = member_data_session.get_selected_columns_as_list
                columns_with_dtypes = member_data_session.get_selected_columns_with_dtypes
                # check if there is no columns picked from the user, delete and reupload the data file
                if len(file_columns) > 1:
                    # row_count = member_data_file.allowed_records_count
                    data_file_rows = get_rows_data_by_search_query(file_path, file_columns, search_query,
                                                                   columns_with_dtypes)
                    # pprint(type(data_file_rows))
                    return Response({"data": data_file_rows, "total_rows": data_file_rows}, status=200,
                                    content_type='application/json')
                else:
                    # delete_data_file(file_path)
                    # delete_all_member_data_file_info(member_data_file)
                    return Response("No Columns in search method", status=200)

        except AttributeError as arex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
            return Response("No Data file uploaded Yet!", status=200)
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())


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
                return Response({"data": data_file_rows, "total_rows": len(data_file_rows)}, status=200,
                                content_type='application/json')
            else:
                delete_data_file(file_path)
                delete_all_member_data_file_info(member_data_file)


        except Exception as ex:
            log_exception(ex)
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
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)

            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
                # cprint(member_data_session, 'green')
                file_path = member_data_session.data_file_path
                columns_with_dtypes = member_data_session.get_selected_columns_with_dtypes
                updated_rows = request.POST.get("rows")

                json_data = json.loads(updated_rows)

                only_used_rows_data = {}
                for key, value in json_data.items():
                    if len(value) > 0:  # check and get the updated rows only
                        only_used_rows_data[key] = value
                        for single in value:
                            tmp_dtype = columns_with_dtypes[single['colName']]
                            # print(single, tmp_dtype)
                            validate = validate_obj.detect_and_validate(single['colValue'], dtype=tmp_dtype)
                            # print(validate)

                column_names = member_data_session.get_selected_columns_as_list
                updated_data = update_rows_data(file_path, only_used_rows_data, column_names, columns_with_dtypes)
                # print(only_used_rows_data)
                if validate['is_error'] is False and "invalid literal for int()" not in updated_data:
                    response = Response({"is_error": False, "msg": updated_data}, status=200,
                                        content_type='application/json')
                else:
                    response = Response({"is_error": True, "msg": updated_data}, status=200,
                                        content_type='application/json')
                return response


        except AttributeError as arex:
            cprint(traceback.format_exc(), 'red')
            log_exception(arex)

            return Response("No Data file uploaded Yet!", status=200)
        except Exception as ex:
            log_exception(ex)
            cprint(traceback.format_exc(), 'red')
            return Response(f"{ex}", status=200)


class DeleteDataFileView(APIView):
    """
    ### Development only ###
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
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int):
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
            else:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=member_data_file.last_uploaded_session)

            delete_data_file(member_data_session.data_file_path)

            member_data_session.delete()

            return Response("File Delete Successfully", status=200)


        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
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
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            member_data_session = None
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            columns = request.POST.get("columns")  # as a dict
            columns_json = json.loads(columns)  # as a dict
            # loop and save only donation fields
            donation_fields = []
            for key, value in columns_json.items():
                if "donation" in value:
                    donation_fields.append(f"'{key}'")
            donation_fields_as_string = f"[{', '.join(donation_fields)}]"
            if isinstance(data_or_num, int) is True:
                # if the member edit exists session
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
            else:
                # here if the member try to upload new session
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=member_data_file.last_uploaded_session)

                # cprint(member_data_session.file_name, 'yellow')
            member_data_session.donation_columns = donation_fields_as_string
            member_data_session.save()
            data_file = member_data_session.data_file_path
            columns_list = member_data_session.get_selected_columns_as_list

            validate_columns_result = validate_data_type_in_dualbox(columns_json, data_file, columns_list)
            # print(validate_columns_result)
            if len(columns_json) > 3:
                return Response({"msg": "THe message is here"}, status=200, content_type='application/json')

            else:
                return Response("Please select at least 3 columns with the data type!", status=200)
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(ex)


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
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file,
                                                                     pk=data_or_num)
                columns_with_dtypes = member_data_session.get_selected_columns_with_dtypes
                column_name = request.POST.get("column_name")
                clicked_row_count = request.POST.get("records_number")
                # clicked_row_count = 50
                all_validate_columns = get_not_validate_rows2(member_data_session.data_file_path, column_name,
                                                              member_data_session.get_selected_columns_as_list,
                                                              columns_with_dtypes, clicked_row_count)
                # return Response("Please wait while validate the date type...", status=200)
                # print(all_validate_columns[0])
                return Response({"data": all_validate_columns, "total_rows": len(all_validate_columns)}, status=200,
                                content_type='application/json')


        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(traceback.format_exc())
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

        except ObjectDoesNotExist as objNotex:
            log_exception(objNotex)
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
            log_exception(ex)
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
        try:
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            if isinstance(data_or_num, int) is True:
                member_data_session = DataHandlerSession.objects.filter(data_handler_id=member_data_file,
                                                                        pk=data_or_num).first()
                # cprint(request.POST, 'blue')
                return Response(member_data_session.file_upload_procedure, status=200)
            else:
                return Response("", status=200)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(ex)


class CheckMemberProcessStatus(APIView):
    """
        ### Developement only ###
        API View to Check if member complete his data handler steps, check if the member run the modal or not

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        from data_handler.models import (DataFile, DataHandlerSession)
        member_data_file = DataFile.objects.get(member=request.user)
        process_status = member_data_file.is_process_complete
        choice = request.POST.get("choice", "")
        params = request.POST.get('parameters')
        data_or_num = check_data_or_num(params)
        # check if it is session number
        if isinstance(data_or_num, int) is True:

            member_session_file = DataHandlerSession.objects.filter(data_handler_id=member_data_file,
                                                                    pk=data_or_num)
        else:
            member_session_file = DataHandlerSession.objects.filter(data_handler_id=member_data_file)

        try:
            if process_status is False:
                if choice != "" or choice is not None:
                    if choice == 'Restore':
                        pass
                    elif choice == 'Fresh':
                        delete_data_file(member_data_file.data_file_path)
                        delete_all_member_data_file_info(member_data_file)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            cprint(str(ex), 'red')
            log_exception(ex)

        # print(process_status)
        return Response(process_status, status=200)


class FetchLastSessionNameView(APIView):
    """
        ### Developement only ###
        API View to get the last session name of the member

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            from data_handler.models import (DataFile, DataHandlerSession)
            member_data_file = DataFile.objects.get(member=request.user)
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            # check if it is session number
            if isinstance(data_or_num, int) is True:
                member_session_file = DataHandlerSession.objects.filter(data_handler_id=member_data_file,
                                                                        pk=data_or_num)
            else:
                member_session_file = DataHandlerSession.objects.filter(data_handler_id=member_data_file)
            session_name = member_session_file.is_process_complete
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(ex)
            cprint(str(ex), 'red')

        # print(process_status)
        return Response(session_name, status=200)


class SetLastSessionName(APIView):
    """
        ### Developement only ###
        API View to set the last session name of the member, last step

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        try:
            from data_handler.models import DataFile, DataHandlerSession
            member_data_file = DataFile.objects.get(member=request.user)
            member_session = DataHandlerSession.objects.filter(data_handler_id=member_data_file)
            session_name = request.POST.get("session_name")
            member_session.current_session_name = session_name
            # member_data_file.session_date_time = parse_datetime(timezone.now())
            member_session.update()


        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            log_exception(ex)
            cprint(str(ex), 'red')

        # print(process_status)
        return Response(session_name, status=200)


class SetSessionLabel(APIView):
    """
        ### Developement only ###
        API View to set the uploaded session label

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        try:
            from datetime import datetime
            from data_handler.models import DataFile, DataHandlerSession
            member_data_file = DataFile.objects.get(member=request.user)
            member_session = DataHandlerSession.objects.get(data_handler_id=member_data_file)
            session_label = request.POST.get("session_label")
            session_task = request.POST.get("session_task", '')
            session_get = request.POST.get('get_session_label', False)
            session_get = bool(session_get)
            # this when member want to check the value of current session in the db
            if session_get is True:
                # check if the session is null return False, True if the session in db
                if member_session.data_handler_session_label == "" or member_session.data_handler_session_label is None:
                    return Response(False, status=200)
                else:
                    return Response(True, status=200)
            elif session_task != '' and session_task == 'set':
                now = datetime.now()
                member_session.data_handler_session_label = session_label
                member_session.session_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                member_session.save()
                return Response('Session label saved successfully!', status=200)

        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            cprint(str(ex), 'red')
            log_exception(ex)


class DeleteSessionView(APIView):
    """
        ### Developement only ###
        API View to set the uploaded session label

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        try:
            from datetime import datetime
            from data_handler.models import DataFile, DataHandlerSession
            member_data_file = DataFile.objects.get(member=request.user)
            session_id = request.POST.get('method')
            if session_id.isdigit():
                member_session = DataHandlerSession.objects.get(data_handler_id=member_data_file, pk=session_id)
                member_session.delete()
            elif session_id == 'all':
                member_session = DataHandlerSession.objects.filter(data_handler_id=member_data_file)
                # cprint(member_session.first().pdf_report_file_path, "green")
                # cprint(member_session.first().csv_report_file_path, "blue")
                # check if the member run the model or not, to remove the model files output
                if member_session.first().is_process_complete:
                    delete_data_file(member_session.first().pdf_report_file_path)
                    delete_data_file(member_session.first().csv_report_file_path)

                for dfile in member_session:
                    delete_data_file(dfile.data_file_path)
                    delete_data_file(dfile.base_data_file_path)
                member_session.delete()
            return Response("Delete Session View", status=200)
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            cprint(str(ex), 'red')
            log_exception(ex)


class RenameSessionView(APIView):
    """
        ### Developement only ###
        API View to rename session

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        try:
            from datetime import datetime
            from data_handler.models import DataFile, DataHandlerSession
            member_data_file = DataFile.objects.get(member=request.user)
            session_name = request.POST.get('session_name')
            params = request.POST.get('parameters')
            data_or_num = check_data_or_num(params)
            # check if it is session number
            if isinstance(data_or_num, int) is True:
                member_session = DataHandlerSession.objects.get(data_handler_id=member_data_file, pk=data_or_num)
                member_session.data_handler_session_label = session_name.strip()
                member_session.save()

            return Response("Session Renamed Successfully!", status=200)
        except Exception as ex:
            cprint(traceback.format_exc(), 'red')
            cprint(str(ex), 'red')
            log_exception(ex)

@login_required
def download_report_file(request, report_type):
    try:
        from data_handler.models import DataFile, DataHandlerSession
        member_data_file = DataFile.objects.get(member=request.user)
        member_session = DataHandlerSession.objects.get(data_handler_id=member_data_file)
        file_path = ""
        mime_type = ''
        if member_session.is_process_complete:

            if report_type == "pdf":
                file_path = member_session.pdf_report_file_path
                mime_type = 'application/pdf'
            elif report_type == 'csv':
                file_path = member_session.csv_report_file_path
                mime_type = "text/csv"
            # cprint(file_path, 'blue')
            # cprint(os.path.exists(file_path), 'red')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type=mime_type)
                    response['Content-Disposition'] = 'attachment; filename=' + smart_str(os.path.basename(file_path))
                    return response

    except Exception as ex:
        cprint(traceback.format_exc(), 'red')
        cprint(str(ex), 'red')
        log_exception(ex)




# class RunModel(APIView):
#     """
#         this api view will run the model
#         """
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, format=None):
#
#         try:
#             from datetime import datetime
#             from data_handler.models import DataFile, DataHandlerSession
#             member_data_file = DataFile.objects.get(member=request.user)
#             data_session = DataHandlerSession.objects.get(data_handler_id=member_data_file)
#             session_name = request.POST.get('session_name')
#             donation_cols = data_session.donation_columns
#             # run_model(data_session.data_file_path, donation_cols)
#             run_model(data_session.base_data_file_path, donation_cols)
#
#             return Response("Session Renamed Successfully!", status=200)
#         except Exception as ex:
#             cprint(traceback.format_exc(), 'red')
#             cprint(str(ex), 'red')
#             log_exception(ex)




