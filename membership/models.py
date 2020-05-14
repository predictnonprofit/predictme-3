from django.db import models
# from users.models import Member
from django.contrib.auth import get_user_model

MEMBER_TYPE = (
    ("starter", "Starter"),
    ("professional", "Professional",),
    ("expert", "Expert")
)

class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBER_TYPE, max_length=20, null=True, blank=True)
    monthly_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    yearly_fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stripe_plane_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    member = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    stripe_member_id = models.CharField(max_length=50)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.member.full_name} -> {self.membership.slug}"


SUB_RANGE = (
    ("monthly", "Monthly"),
    ("yearly", "Yearly",),
)

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    # plan = models.OneToOneField(Plan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=60, null=True, blank=True)
    active = models.BooleanField()
    sub_range = models.CharField(max_length=20, choices=SUB_RANGE, null=True, blank=True)
    subscription_start_date = models.DateField(blank=True, null=True)
    subscription_end_date = models.DateField(blank=True, null=True)





