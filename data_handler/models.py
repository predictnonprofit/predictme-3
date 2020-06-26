from django.db import models
# from membership.models import UserMembership
# Create your models here.
from django.contrib.auth import get_user_model

UPLOAD_PROCEDURES = (
    ("local_file", "Local File"),
    ("google_plus", "Google Plus",),
    ("one_drive", "One Drive"),
    ("dropbox", "Dropbox"),
    ("none", "None")
)


class DataFile(models.Model):
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                               related_name='member_data_file')
    file_upload_procedure = models.CharField(max_length=20, null=True, blank=True, choices=UPLOAD_PROCEDURES)
    data_file_path = models.CharField(max_length=255, blank=True, null=True)
    all_records_count = models.BigIntegerField(null=True, blank=True)
    allowed_records_count = models.IntegerField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now=True)
    join_date = models.DateTimeField(auto_now_add=True)
    selected_columns = models.TextField(null=True, blank=True)

    class Meta:
        # verbose_name = "member_data_file"
        db_table = 'member_data_files'

    def __str__(self):
        return f"{self.data_file_path}"

    @property
    def get_selected_columns_as_list(self):
        # return self.selected_columns.split("|")
        return sorted(self.selected_columns.split("|"))


class MemberDownloadCounter(models.Model):
    member = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True,
                               related_name='download_counter')
    is_accept_terms = models.BooleanField(null=True, blank=True, default=False)
    is_accept_download_template = models.BooleanField(null=True, blank=True, default=False)  # this when the member check he download
    is_download_template = models.BooleanField(null=True, blank=True, default=False)  # this if the member download the template or not
    download_counter = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        db_table = 'members_download_counter'
