# Model/generator.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import spacy
import os
from datetime import datetime
from audio_generator import generate_audio

# Chargement du modèle GPT-2 français
MODEL_NAME = "dbddv01/gpt2-french-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Chargement du modèle spaCy français (optionnel pour extraction)
# nlp = spacy.load("fr_core_news_md")

def build_prompt(name=None, creature=None, place=None):
    name = name or "Lina"
    creature = creature or "petite chouette"
    place = place or "forêt enchantée"
    return f"{name} est une {creature} qui vit dans une {place}. Un jour, quelque chose d’étrange se passe..."

def generate_story(prompt, max_length=250, temperature=0.9, top_p=0.9):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=1.2,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    story = tokenizer.decode(output[0], skip_special_tokens=True)
    return story.replace(prompt, "", 1).strip()

def generate_story_with_audio(prompt, audio_enabled=False):
    story = generate_story(prompt)
    audio_path = None
    if audio_enabled:
        safe_filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        audio_path = generate_audio(story, filename=safe_filename)
    return story, audio_path

# Exemple d'utilisation
if __name__ == "__main__":
    prompt = build_prompt(name="Tilo", creature="petit dragon", place="village perché sur la montagne")
    story, audio = generate_story_with_audio(prompt, audio_enabled=True)
    print("\nHistoire générée :\n")
    print(story)
    if audio:
        print(f"\nAudio enregistré ici : {audio}")

