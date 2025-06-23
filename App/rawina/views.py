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
    fields = ['title', 'content']
    success_url = reverse_lazy('rawina:story_list')
