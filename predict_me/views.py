from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View
from membership.models import (Membership, UserMembership, Subscription)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'predict_me/about.html'


class ContactView(TemplateView):
    template_name = 'predict_me/contact.html'

class FAQView(TemplateView):
    template_name = 'predict_me/faq.html'


class PricingView(View):
    def get(self, request):
        return render(request, "predict_me/pricing.html")

    def post(self, request):
        member_type = request.POST['type']
        member = request.user
        membership = Membership.objects.get(membership_type=member_type)
        user_membership = UserMembership()
        user_membership.member = member
        user_membership.membership = membership
        user_membership.save()
        # messages.success(request, f"The plan you selected is {membership.membership_type} plan")
        return redirect(reverse("checkout"))


class ModelDescView(TemplateView):
    template_name = 'predict_me/model_description.html'

class LandPageView(TemplateView):
    template_name = 'predict_me/land_page.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'predict_me/privacy_policy.html'

class TermsView(TemplateView):
    template_name = 'predict_me/terms.html'

def error_503(request):
    return render(request, "predict_me/errors/503.html")