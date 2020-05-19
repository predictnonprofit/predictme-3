from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .helpers import extract_columns_names

class DataListView(TemplateView):
    template_name = "data_handler/list.html"


@api_view(['POST'])
def data_handler_init(request):
    if request.method == "POST":
        picked_columns = request.POST.get("columns")
        print()
        return Response(request.POST)


@api_view(['POST'])
def data_handler_file_upload(request):
    if request.method == "POST":
        data_file = request.FILES.get("doner_file");
        print()
        return Response(request.POST)


class DataHandlerFileUpload(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (FileUploadParser,)

    def post(self, request, filename, format=None):
        data_file_obj = request.FILES['file']

        #  Saving PUT'ed file to storage
        # file_name = default_storage.save(data_file_obj.name, data_file_obj)  # this will return the file name only
        #  Reading file from storage to get the file url
        # file = default_storage.open(file_name)
        # file_url = default_storage.url(file_name)
        fs = FileSystemStorage()
        filename = fs.save(data_file_obj.name, data_file_obj)
        uploaded_file_url = fs.url(filename)
        # columns_names = extract_columns_names(filename)
        # print(columns_names)
        return Response("ok", status=200)
        # return Response(columns_names)
