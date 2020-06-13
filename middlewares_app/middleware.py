from django.urls import reverse
from django.http import HttpResponseRedirect


class CheckMemberStatus:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # print(request.user.is_authenticated)

        # print(request.path)
        if request.user.is_authenticated:
            print(request.user.status)
            if request.user.status == "pending":
                return HttpResponseRedirect(reverse("users_pending"))
            elif request.user.status == "unverified":
                return HttpResponseRedirect(reverse("users_pending"))

        return response

    # def process_request(self, request):
    #     print("MY MIDDLE WARE")
