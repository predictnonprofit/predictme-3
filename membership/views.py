from django.shortcuts import (render, redirect, reverse, HttpResponse)
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
import os
from datetime import datetime
from dateutil.relativedelta import *
from .models import (Subscription, UserMembership, Membership)
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class CheckoutView(View):
    template_name = "membership/checkout.html"

    def get(self, request):
        user_membership = UserMembership.objects.get(member=request.user)
        return render(request, "membership/checkout.html", context={"user_membership": user_membership})

    def post(self, request):

        if request.method == "POST":
            print(request.POST)
            member = request.user
            sub_range = request.POST.get("sub_range")
            payment_agree = request.POST.get("agree_payment")
            stripe_token = request.POST.get("stripeToken")
            member.stripe_card_token = stripe_token
            member.status = "active"
            member.save()
            usermembership = UserMembership.objects.get(member=member)

            # new_member_subscription_stripe_id = stripe.Subscription.create(
            #     customer=member.stripe_customer_id,
            #     default_payment_method="pm_card_visa",
            #     items=[
            #         {"plan": usermembership.membership.stripe_plane_id},
            #         ]
            #     )

            # sub_start_date = datetime.now()
            # sub_end_date = sub_start_date + relativedelta(months=+1)
            # subscription = Subscription(member=member, stripe_subscription_id=new_member_subscription_stripe_id['id'],
            #                               active=True, sub_range=sub_range, subscription_start_date=sub_start_date,
            #                               subscription_end_date=sub_end_date)
            #
            # print(f"Subscription done: {new_member_subscription_stripe_id}")
              # print(new_member_stripe_id['id'])
              # return HttpResponse(new_member_stripe_id['id'])
            return redirect(reverse("register_successfully"))



class RegisterSuccessfully(TemplateView):
    template_name = "membership/inc/payment_success.html"
