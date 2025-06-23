from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    HomeView,
    RegisterView,
    LoginView,
    AccountSettingsView,
    EditProfileView,
    ChangePasswordView
)

app_name = "user"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("account/", AccountSettingsView.as_view(), name="account_settings"),
    path("edit_profile/", EditProfileView.as_view(), name="edit_profile"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
]