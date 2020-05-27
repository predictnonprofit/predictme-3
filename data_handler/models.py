from django.db import models
from membership.models import UserMembership
# Create your models here.

UPLOAD_PROCEDURES = (
    ("local_file", "Local File"),
    ("google_plus", "Google Plus",),
    ("one_drive", "One Drive"),
    ("dropbox", "Dropbox")
)

class MemberDataFile(models.Model):
    membership = models.OneToOneField(UserMembership, null=True, blank=True, on_delete=models.CASCADE, related_name="member_data_file")
    file_upload_procedure = models.CharField(max_length=20, null=True, blank=True, choices=UPLOAD_PROCEDURES)
    data_file_path = models.CharField(max_length=255, blank=True, null=True)
    all_records_count = models.BigIntegerField(null=True, blank=True)
    allowed_records_count = models.IntegerField(null=True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "member_data_file"
        db_table = 'member_data_file'

    def __str__(self):
        return f"{self.membership.member.email}"



