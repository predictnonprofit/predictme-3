from django.db import models
from membership.models import UserMembership
# Create your models here.


class MemberData(models.Model):
    member = models.OneToOneField(UserMembership, null=True, blank=True, on_delete=models.CASCADE)
    # file will be saved to MEDIA_ROOT/uploads/2015/01/30
    data_file_path = models.FileField(upload_to="members_data/%Y/%m/%d/", null=True, blank=True)
    all_records_count = models.BigIntegerField(null=True, blank=True)
    allowed_records_count = models.IntegerField(null=True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)


