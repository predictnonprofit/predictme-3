from django.views.generic import TemplateView



class ProfileOverview(TemplateView):
    template_name = "members_app/profile/overview.html"

class ProfilePersonal(TemplateView):
    template_name = "members_app/profile/personal.html"

class ProfileInformation(TemplateView):
    template_name = "members_app/profile/information.html"

class ProfileChangePassword(TemplateView):
    template_name = "members_app/profile/change-password.html"

class ProfileEmail(TemplateView):
    template_name = "members_app/profile/email.html"

class SubscriptionManageView(TemplateView):
    template_name = "members_app/profile/subscription.html"