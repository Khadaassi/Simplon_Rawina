import os

import requests
from dotenv import load_dotenv
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.edit import FormView

from .forms import StoryGenerationForm, ChooseThemeForm
from .models import Story


load_dotenv()

API_URL = os.getenv("RAWINA_API_URL")


# Create your views here.
class DashboardView(TemplateView):
    template_name = "rawina/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["stories"] = Story.objects.filter(user=self.request.user).order_by(
                "-created_at"
            )[:3]
        return context


class StoryListView(ListView):
    model = Story
    template_name = "rawina/story_list.html"
    context_object_name = "stories"

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if "pdf" in request.GET and "id" in request.GET:
            story = Story.objects.get(id=request.GET.get("id"), user=request.user)
            html = render_to_string("rawina/story_pdf.html", {"story": story})
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="{story.title}.pdf"'
            )
            pisa.CreatePDF(html, dest=response)
            return response

        return super().get(request, *args, **kwargs)


class StoryCreateView(FormView):
    template_name = "rawina/create_story.html"
    form_class = StoryGenerationForm

    def get_initial(self):
        initial = super().get_initial()
        theme = self.request.GET.get("theme")
        if theme:
            initial["theme"] = theme
        return initial

    def form_valid(self, form):
        # Récupère les données du formulaire
        name = form.cleaned_data["name"]
        character = form.cleaned_data["character"]
        place = form.cleaned_data["place"]
        theme = form.cleaned_data["theme"]
        title = f"{name.capitalize()}'s Story"

        # Prépare le payload pour l'API
        payload = {
            "user_id": str(self.request.user.id),
            "theme": theme,
            "name": name,
            "creature": character,
            "place": place,
            "audio": False,
        }

        # Appel à l'API FastAPI
        try:
            resp = requests.post(API_URL, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            generated_text = data.get("story", "")
            audio_path = data.get("audio_path")
        except Exception as e:
            form.add_error(None, "Could not generate story. Please try again later.")
            return self.form_invalid(form)


        # Création de l'objet Story en base
        story = Story.objects.create(
            user=self.request.user,
            title=title,
            theme=theme,
            prompt="",  # si tu veux stocker le prompt d'appel, tu peux le mettre ici
            generated_text=generated_text,
            audio_url=audio_path,
        )

        # Affiche la page de loading avant redirection
        return render(
            self.request,
            "rawina/loading_story.html",
            {
                "redirect_url": reverse("rawina:story", kwargs={"pk": story.pk}),
                "delay": 3000,
            },
        )


class ChooseThemeView(FormView):
    template_name = "rawina/choose_theme.html"
    form_class = ChooseThemeForm

    def form_valid(self, form):
        selected_theme = form.cleaned_data["theme"]
        return redirect(f"{reverse_lazy('rawina:create')}?theme={selected_theme}")


class StoryDetailView(TemplateView):
    template_name = "rawina/story_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story_id = self.kwargs.get("pk")
        context["story"] = Story.objects.get(id=story_id)
        return context


class StoryDeleteView(TemplateView):
    template_name = "rawina/story_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story_id = self.kwargs.get("pk")
        context["story"] = Story.objects.get(id=story_id)
        return context

    def post(self, request, *args, **kwargs):
        story_id = self.kwargs.get("pk")
        story = Story.objects.get(id=story_id)
        if story.user == request.user:
            story.delete()
            return redirect(reverse("rawina:story_list"))
        return redirect(reverse("rawina:dashboard"))

