from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager



MEMBER_STATUS = (
    ("pending", "Pending"),
    ('active', "Active"),
    ("cancelled", "Cancelled"),
    ("unverified", "Un-Verified")
)

class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=50, null=True, blank=True)
    street_address = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    org_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50, blank=True, null=True)
    org_website = models.URLField(max_length=100, blank=True, null=True)
    org_type = models.CharField(max_length=50)
    annual_revenue = models.CharField(max_length=200)
    total_staff = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    num_of_volunteer = models.IntegerField(null=True, blank=True)
    num_of_board_members = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=MEMBER_STATUS, default="unverified")
    # membership = models.OneToOneField(to="membership.Membership", null=True, on_delete=models.CASCADE, blank=True)
    member_register_token = models.CharField(max_length=150, null=True, blank=True)
    stripe_card_token = models.CharField(max_length=200, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "members"




class UnverifiedMember(models.Model):
     member = models.OneToOneField(Member, on_delete=models.CASCADE)
     join_date = models.DateTimeField(auto_now_add=True)

     class Meta:
        db_table = "unverified_member"
