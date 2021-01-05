from django.shortcuts import (render, redirect, reverse, HttpResponse)
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
import os
from datetime import datetime
from dateutil.relativedelta import *
from .models import (Subscription, UserMembership, Membership)
from termcolor import cprint
from prettyprinter import pprint
import stripe
import os
import datetime
import pytz
from django.db.models import Q

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class CheckoutView(View):
    template_name = "membership/checkout.html"

    def get(self, request):
        stripe_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
        subscription = Subscription.objects.get(member_id=request.user)
        return render(request, "membership/checkout.html",
                      context={"subscription": subscription, "stripe_key": stripe_key})

    def post(self, request):
        if request.method == "POST":
            member = request.user
            # cprint(request.POST, "cyan")
            sub_range = request.POST.get("sub_range")
            payment_agree = request.POST.get("agree_payment")
            stripe_token = request.POST.get("stripeToken")
            member.stripe_card_token = stripe_token
            member.status = "active"
            member.save()
            # id, created, plan[interval], plan[product], price[active], latest_invoice, status, current_period_end
            # current_period_start, customer
            subscription = Subscription.objects.get(member_id=member)
            # cprint(subscription.stripe_plan_id, 'blue')
            membership = Membership.objects.filter(
                Q(range_label=sub_range) & Q(parent=subscription.stripe_plan_id.slug)).first()
            subscription.stripe_plan_id = membership
            subscription.save()
            # cprint(subscription.stripe_plan_id, 'magenta')
            customer = stripe.Customer.modify(
                subscription.member_id.stripe_customer_id,
                card=stripe_token
            )
            member.stripe_customer_id = customer['id']
            member.save()
            stripe_subscription_obj = stripe.Subscription.create(
                customer=customer['id'],
                items=[
                    {"price": subscription.stripe_plan_id.stripe_price_id},
                    # {"price_data": {
                    #     "product": subscription.stripe_plan_id.stripe_plane_id,
                    #     "currency": "usd"
                    # }},
                ],
            )
            tmp_customer = stripe.Customer.retrieve(customer['id'])
            card_id = tmp_customer['default_source']
            subscription.stripe_subscription_id = stripe_subscription_obj['id']
            subscription.stripe_card_id = card_id
            card_obj = stripe.Customer.retrieve_source(customer['id'], card_id)
            start_date = datetime.datetime.fromtimestamp(stripe_subscription_obj['current_period_start'],
                                                         tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
            end_date = datetime.datetime.fromtimestamp(stripe_subscription_obj['current_period_end'],
                                                       tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")
            subscription.subscription_status = True if stripe_subscription_obj['status'] == "active" else False
            subscription.subscription_period_start = start_date
            subscription.subscription_period_end = end_date
            subscription.card_last_4_digits = card_obj['last4']
            subscription.card_brand = card_obj['brand']
            subscription.card_expire = datetime.datetime(card_obj['exp_year'], card_obj['exp_month'], 1)
            subscription.sub_range = sub_range

            subscription.save()

            return redirect(reverse("register_successfully"))
            # return JsonResponse(data={"status": "register Done"}, status=200)


class RegisterSuccessfully(TemplateView):
    template_name = "membership/inc/payment_success.html"
