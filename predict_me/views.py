from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View
from membership.models import (Membership, UserMembership, Subscription)
from data_handler.models import (DataFile)
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
        # print(member_type)
        member = request.user
        # print(member.full_name)
        membership = Membership.objects.get(slug=member_type)
        member_data_file = DataFile.objects.get(member=member)
        # print(membership)
        user_membership = UserMembership.objects.get(member=member)
        user_membership.membership = membership
        member_data_file.allowed_records_count = membership.allowed_records_count
        user_membership.save()
        member_data_file.save()
        # print(user_membership.membership)

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
