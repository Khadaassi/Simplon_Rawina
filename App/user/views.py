from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import RegistrationForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'user/home.html'

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
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('user:home')
    
