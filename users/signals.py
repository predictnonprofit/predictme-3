from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from membership.models import UserMembership
import stripe
# user_member_obj = get_user_model()


def create_usermembership(sender, instance, created, **kwargs):
    if created:
        UserMembership.objects.get_or_create(member=instance)

    user_membership_obj, created = UserMembership.objects.get_or_create(member=instance)

    # check if the new member has stripe id
    if user_membership_obj.stripe_member_id is None or user_membership_obj.stripe_member_id == "":
        new_member_id = stripe.Customer.create(email=instance.email)
        user_membership_obj.stripe_member_id = new_member_id['id']
        user_membership_obj.save()

# post_save.connect(create_usermembership, sender=get_user_model())


