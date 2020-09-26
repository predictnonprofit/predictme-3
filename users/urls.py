from django.urls import path, include, re_path
from .views import *
from membership.views import CheckoutView, RegisterSuccessfully

# app_name = "users"

urlpatterns = [
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register_view, name="register"),
    path("checkout", CheckoutView.as_view(), name="checkout"),
    path("success", RegisterSuccessfully.as_view(), name="register_successfully"),
    path("complete", CompleteRegister.as_view(), name="register-complete"),
    path("pending", PendingUserView.as_view(), name="users_pending"),
    path("canceled", CancelUserView.as_view(), name="users_canceled"),
    path("verify", VerifyAccountView.as_view(), name="users_verify"),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         activate_account, name='activate'),
    path(r'activate/<uidb64>/<token>/', activate_account, name='activate'),
    path("google", GoogleAuthenticationView.as_view(), name="auth-google"),

]