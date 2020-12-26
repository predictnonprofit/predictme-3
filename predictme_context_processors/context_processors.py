def get_user_subscription(request):
    if request.user.is_authenticated:
        from membership.models import Subscription

        try:
            subscription_obj = Subscription.objects.get(member_id=request.user)
        except Subscription.DoesNotExist:
            subscription_obj = None
        return subscription_obj


def get_data_handler_obj(request):
    if request.user.is_authenticated:
        from data_handler.models import DataFile
        data_handler_obj = DataFile.objects.get(member=request.user)
        return data_handler_obj


def get_data_handler_and_session(request):
    if request.user.is_authenticated:
        from data_handler.models import (DataFile, DataHandlerSession)
        data_handler_obj = DataFile.objects.filter(member=request.user).first()
        data_session_obj = DataHandlerSession.objects.filter(data_handler_id=data_handler_obj).first()
        return {
            "data_obj": data_handler_obj,
            "session_obj": data_session_obj
        }


def get_all_member_objects(request):
    """
    this function will return dictionary of all user data (subscription, data handler, data handler session, and member) objects
    """
    if request.user.is_authenticated:
        from data_handler.models import (DataFile, DataHandlerSession)
        from membership.models import (Subscription)
        from users.models import Member
        all_objs = {}
        member_obj = Member.objects.get(pk=request.user.pk)
        try:
            subscription_obj = Subscription.objects.get(member_id=request.user)
        except Subscription.DoesNotExist:
            subscription_obj = None
        data_handler_obj = DataFile.objects.get(member=request.user)
        try:
            data_handler_session = DataHandlerSession.objects.get(data_handler_id=data_handler_obj)
        except DataHandlerSession.DoesNotExist:
            data_handler_session = None
        all_objs['MEMBER'] = member_obj
        all_objs['SUBSCRIPTION'] = subscription_obj
        all_objs['DATA_HANDLER'] = data_handler_obj
        all_objs['DATA_HANDLER_SESSION'] = data_handler_session

        return all_objs


def return_all_context(request):
    return {
        "get_user_membership": get_user_subscription(request),  # fix this in all places that call it
        "get_data_handler_obj": get_data_handler_obj(request),
        "get_all_member_info": get_all_member_objects(request),
        "get_data_handler_and_session": get_data_handler_and_session(request),
    }
