from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from .models import Story  # Assuming you have a Story model defined in models.py

# Create your views here.
class DashboardView(TemplateView):
    template_name = "rawina/dashboard.html"

class StoryListView(ListView):
    model = Story
    template_name = "rawina/story_list.html"
    context_object_name = "stories"

class StoryCreateView(CreateView):
    model = Story
    template_name = "rawina/story_form.html"
    fields = ['name','character', 'place', 'theme']
    success_url = reverse_lazy('rawina:story_list')

class ChooseThemeView(TemplateView):
    template_name = "rawina/choose_theme.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = ['Theme 1', 'Theme 2', 'Theme 3']
        return context