from django.db import models
from django.contrib.auth import get_user_model
from data_handler.models import DataFile, DataHandlerSession

MEMBERSHIP_LABELS = (
    ("starter", "Starter"),
    ("professional", "Professional",),
    ("expert", "Expert")
)

SUB_RANGE = (
    ("monthly", "Monthly"),
    ("yearly", "Yearly",),
)


class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True, db_index=True)
    membership_type = models.CharField(choices=MEMBERSHIP_LABELS, max_length=20, null=True, blank=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stripe_plane_id = models.CharField(max_length=100, null=True, blank=True)
    additional_fee_per_extra_record = models.DecimalField(max_digits=2, decimal_places=2, null=True, blank=True)
    allowed_records_count = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.membership_type


class Subscription(models.Model):
    member_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="member_subscription",
                                  null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=60, null=True, blank=True)
    stripe_plan_id = models.ForeignKey(Membership, on_delete=models.CASCADE, blank=True, null=True)
    subscription_status = models.BooleanField(null=True, blank=True)
    subscription_period_start = models.DateTimeField(null=True, blank=True)
    subscription_period_end = models.DateTimeField(null=True, blank=True)
    card_expire = models.DateTimeField(null=True, blank=True)
    sub_range = models.CharField(max_length=20, choices=SUB_RANGE, null=True, blank=True)
    card_brand = models.CharField(max_length=30, null=True, blank=True)
    card_last_4_digits = models.CharField(max_length=5, null=True, blank=True)
    stripe_card_id = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"{self.member_id} Subscription Object"

    class Meta:
        db_table = "subscriptions"


class UserMembership(models.Model):
    """
    Model can access to member with its membership and data file
    """
    member = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True,
                                  related_name="user_membership")
    stripe_member_id = models.CharField(max_length=50)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="membership")
    data_file_obj = models.ForeignKey(DataFile, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="data_file")
    subscription_obj = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name="sub_obj")

    def __str__(self):
        return f"User Membership of {self.member.email}"

    class Meta:
        db_table = "user_membership"
