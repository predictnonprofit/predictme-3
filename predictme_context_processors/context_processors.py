def get_user_membership(request):
    if request.user.is_authenticated:
        from membership.models import UserMembership
        user_membership = UserMembership.objects.get(member=request.user)
        return user_membership


def return_all_context(request):
    return {
        "get_user_membership": get_user_membership(request),
    }
