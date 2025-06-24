from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import StoryGenerationForm, ChooseThemeForm
from .models import Story

# Create your views here.
class DashboardView(TemplateView):
    template_name = "rawina/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['stories'] = Story.objects.filter(user=self.request.user).order_by('-created_at')[:3]
        return context

class StoryListView(ListView):
    model = Story
    template_name = "rawina/story_list.html"
    context_object_name = "stories"

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user).order_by('-created_at')


class StoryCreateView(FormView):
    template_name = 'rawina/create_story.html'
    form_class = StoryGenerationForm

    def get_initial(self):
        initial = super().get_initial()
        theme = self.request.GET.get('theme')
        if theme:
            initial['theme'] = theme
        return initial

    def form_valid(self, form):
        name = form.cleaned_data['name']
        character = form.cleaned_data['character']
        place = form.cleaned_data['place']
        theme = form.cleaned_data['theme']

        prompt = f"{name} wants to hear a story about {character} in {place} — a {theme} adventure."
        generated_text = "Once upon a time..."

        story = Story.objects.create(
            user=self.request.user,
            title=f"{character}'s Story",
            theme=theme,
            prompt=prompt,
            generated_text=generated_text
        )

        return redirect(reverse('rawina:story', kwargs={'pk': story.pk}))

class ChooseThemeView(FormView):
    template_name = 'rawina/choose_theme.html'
    form_class = ChooseThemeForm
    

    def form_valid(self, form):
        selected_theme = form.cleaned_data['theme']
        return redirect(f"{reverse_lazy('rawina:create')}?theme={selected_theme}")
        


class StoryDetailView(TemplateView):
    template_name = 'rawina/story_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story_id = self.kwargs.get('pk')
        context['story'] = Story.objects.get(id=story_id)
        return context