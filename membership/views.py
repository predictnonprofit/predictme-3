from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from .models import (Subscription, UserMembership, Membership)
import os
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class CheckoutView(View):
    template_name = "membership/checkout.html"

    def get(self, request):
        member = request.user
        return render(request, "membership/checkout.html", context={"member": member})

    def post(self, request):
        if request.method == "POST":
            print(request.POST)
            member = request.user
            sub_range = request.POST.get("sub_range")
            payment_agree = request.POST.get("agree_payment")
            usermembership = UserMembership.objects.get(member=member)
            new_member_stripe_id = stripe.Customer.create(email=member.email, name=member.full_name)
            usermembership.stripe_member_id = new_member_stripe_id['id']
            usermembership.save()
            member.status = "active"
            #
            # print(new_member_stripe_id['id'])
            # return HttpResponse(new_member_stripe_id['id'])
            return redirect(reverse("register_successfully"))


class RegisterSuccessfully(TemplateView):
    template_name = "membership/inc/payment_success.html"


