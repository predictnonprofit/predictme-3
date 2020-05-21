from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .helpers import handle_uploaded_file
import os


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
        data_file = request.FILES.get("doner_file")
        print(request.POST)
        return Response(request.FILES)


class DataHandlerFileUpload(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, filename, format=None):
        # data_file_obj = request.FILES['file']
        dfile = request.FILES['donor_file']

        path = default_storage.save(f"data/{dfile.name}", ContentFile(dfile.read()))
        tmp_file = os.path.join(settings.MEDIA_URL, path)
        thefile = default_storage.open(path)
        columns = extracted_columns(thefile)
        return Response(columns, status=200)
        # return Response(columns_names)
