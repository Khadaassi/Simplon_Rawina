from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    HomeView,
    RegisterView,
    LoginView,
)
app_name = "user"
urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]