from django.views.generic import TemplateView, View
from rest_framework.decorators import api_view
from django.shortcuts import render
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
from .helpers import handle_uploaded_file, extract_columns_names
import os
from .models import MemberDataFile
from membership.models import UserMembership


class DataListView(View):
    template_name = "data_handler/list.html"
    def get(self, request, *args, **kwargs):
        usermembership = UserMembership.objects.get(member=request.user)
        context = {'member_data_file': MemberDataFile.objects.get(membership=usermembership)}
        return render(request, "data_handler/list.html", context=context)




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
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        thefile = default_storage.open(path)
        # print(tmp_file)
        columns = extract_columns_names(tmp_file)
        return Response(columns, status=200)
        # return Response(columns_names)


class RecordsColumnView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        # data_file_obj = request.FILES['file']
        columns_names = request.POST['columns']

        
        return Response(str(columns_names), status=200)
        # return Response(columns_names)
