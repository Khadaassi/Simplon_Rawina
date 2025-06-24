from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    THEME_CHOICES = [
        ('animals', 'Animals'),
        ('fantasy', 'Fantasy'),
        ('daily_hero', 'Daily Hero'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=100, help_text="Titre de l’histoire")
    theme = models.CharField(max_length=20, choices=THEME_CHOICES)
    prompt = models.TextField(help_text="Prompt utilisé pour générer l'histoire")
    generated_text = models.TextField(help_text="Texte généré par le modèle")

    images = models.JSONField(blank=True, null=True, help_text="Liste d'URLs ou chemins d'images")
    audio_url = models.URLField(blank=True, null=True, help_text="Lien vers le fichier audio généré")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} – {self.user.username} ({self.created_at.date()})"
