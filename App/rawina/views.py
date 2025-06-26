import os
import requests
import threading
from dotenv import load_dotenv
from xhtml2pdf import pisa

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView

from .forms import StoryGenerationForm, ChooseThemeForm
from .models import Story


# charge .env
load_dotenv()
API_URL = os.getenv("RAWINA_API_URL")


def _generate_and_save(story_id, payload):
    """
    Tâche de fond : appelle l’API et met à jour `generated_text` (+ audio_url).
    """
    try:
        resp = requests.post(API_URL, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("story", "")
        audio = data.get("audio_path")
    except Exception:
        text, audio = "⚠️ Failed to generate story.", None

    story = Story.objects.get(pk=story_id)
    story.generated_text = text
    if audio:
        story.audio_url = audio
    story.save()


class DashboardView(TemplateView):
    template_name = "rawina/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx["stories"] = Story.objects.filter(user=self.request.user) \
                                        .order_by("-created_at")[:3]
        return ctx


class StoryListView(ListView):
    model = Story
    template_name = "rawina/story_list.html"
    context_object_name = "stories"

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user).order_by("-created_at")

    def get(self, request, *args, **kwargs):
        # téléchargement PDF à la volée si on passe ?pdf=1&id=...
        if request.GET.get("pdf") and request.GET.get("id"):
            story = get_object_or_404(Story, id=request.GET["id"], user=request.user)
            html = render_to_string("rawina/story_pdf.html", {"story": story})
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{story.title}.pdf"'
            pisa.CreatePDF(html, dest=response)
            return response
        return super().get(request, *args, **kwargs)


class StoryDetailView(DetailView):
    model = Story
    template_name = "rawina/story_detail.html"
    context_object_name = "story"

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)


class ChooseThemeView(FormView):
    template_name = "rawina/choose_theme.html"
    form_class = ChooseThemeForm

    def form_valid(self, form):
        selected = form.cleaned_data["theme"]
        return redirect(f"{reverse('rawina:create')}?theme={selected}")


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
        # prépare le payload
        payload = {
            "user_id": str(self.request.user.id),
            "theme": form.cleaned_data["theme"],
            "name": form.cleaned_data["name"],
            "creature": form.cleaned_data["character"],
            "place": form.cleaned_data["place"],
            "audio": True,
        }

        # crée un placeholder vide
        story = Story.objects.create(
            user=self.request.user,
            title=f"{form.cleaned_data['name'].capitalize()}'s Story",
            theme=payload["theme"],
            prompt="",   # ou stocke ici ton prompt
            generated_text="",
        )

        # lance la génération en background
        threading.Thread(
            target=_generate_and_save,
            args=(story.pk, payload),
            daemon=True
        ).start()

        # renvoie la page de loading (JS de polling utilisera StoryStatusView)
        return render(self.request, "rawina/loading_story.html", {
            "story_id": story.pk,
        })


class StoryStatusView(View):
    """
    End-point JSON pour le polling de loading_story.html :
    renvoie { ready: bool, url: "<detail_url>" }
    """
    def get(self, request, pk):
        story = get_object_or_404(Story, pk=pk, user=request.user)
        return JsonResponse({
            "ready": bool(story.generated_text),
            "url": reverse("rawina:story", kwargs={"pk": story.pk})
        })


class StoryDeleteView(View):
    """
    Supprime la story et redirige selon le résultat.
    """
    def post(self, request, pk):
        story = get_object_or_404(Story, pk=pk, user=request.user)
        story.delete()
        return redirect(reverse("rawina:story_list"))
