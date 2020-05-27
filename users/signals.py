from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.contrib.auth import get_user_model
from membership.models import UserMembership
from data_handler.models import MemberDataFile
import stripe
# user_member_obj = get_user_model()



def create_usermembership_memberdatafile(sender, instance, created, **kwargs):
    """
    this function will run after new member register, to create usermembership 
    object to the new member,
    Arguments:
        sender {[type]} -- [description]
        instance {[type]} -- [description]
        created {[type]} -- [description]
    """
    try:
        if created:
            UserMembership.objects.get_or_create(member=instance)

        user_membership_obj, created = UserMembership.objects.get_or_create(member=instance)

        # check if the new member has stripe id
        if user_membership_obj.stripe_member_id is None or user_membership_obj.stripe_member_id == "":
            new_member_id = stripe.Customer.create(email=instance.email)
            user_membership_obj.stripe_member_id = new_member_id['id']
            user_membership_obj.save()

        # create memberdatafile object for the new member
        memberdatafile_obj, created = MemberDataFile.objects.get_or_create(member=user_membership_obj)
        memberdatafile_obj.save()

    except ex as ObjectDoesNotExist:
        return HttpResponseNotFound("Oops! Member Not found!")
    else:
        print("members data file, usermembership are created successfuly!")


post_save.connect(create_usermembership_memberdatafile, sender=get_user_model())


