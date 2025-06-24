from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import RegistrationForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'user/home.html'
    success_url = reverse_lazy('user:login')

class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
class LoginView(AuthLoginView):
    template_name = 'user/login.html'
    # redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('rawina:dashboard')

class AccountSettingsView(TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(TemplateView):
    template_name = 'user/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        # Handle profile update logic here
        return redirect('user:account_settings')

class ChangePasswordView(TemplateView):
    template_name = 'user/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        # Handle password change logic here
        return redirect('user:account_settings')