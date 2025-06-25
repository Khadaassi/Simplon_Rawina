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
        title = f"{name.capitalize()}'s Story"

        prompt = f"Write a story about {name}, a {character} in {place} — a {theme} adventure."
        generated_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce porttitor, orci non commodo tincidunt, sapien turpis euismod est, ut dapibus diam lorem ac eros. Mauris et fermentum urna. Integer eu sem eu erat posuere rhoncus. Aliquam erat volutpat. Cras congue, neque ac aliquam fermentum, tellus nulla sodales lorem, non efficitur lorem velit sed nisi. Nullam tincidunt, lacus at gravida tincidunt, elit risus rhoncus velit, nec egestas nisl dolor a nisi. Morbi hendrerit ut elit id gravida. Suspendisse."

        story = Story.objects.create(
            user=self.request.user,
            title=title,
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

class StoryDeleteView(TemplateView):
    template_name = 'rawina/story_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story_id = self.kwargs.get('pk')
        context['story'] = Story.objects.get(id=story_id)
        return context

    def post(self, request, *args, **kwargs):
        story_id = self.kwargs.get('pk')
        story = Story.objects.get(id=story_id)
        if story.user == request.user:
            story.delete()
            return redirect(reverse('rawina:story_list'))
        return redirect(reverse('rawina:dashboard'))