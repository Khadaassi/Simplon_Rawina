from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from datetime import datetime
from audio_generator import generate_audio

# Chargement du modèle fine-tuné en anglais
MODEL_PATH = "gpt2-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

def build_prompt(name=None, creature=None, place=None):
    name = name or "Lina"
    creature = creature or "little owl"
    place = place or "enchanted forest"
    return (
        f"Theme: animals\n"
        f"Story: This is a short and cheerful story for kids.\n"
        f"{name} is a {creature} who lives in a {place}. One day, something unusual happens..."
    )

def generate_story(prompt, max_length=450, temperature=0.9, top_p=0.9):
    encoded = tokenizer(prompt, return_tensors="pt", padding=True)
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]  # ✅ déclaration ici

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
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
    prompt = build_prompt(name="Tilo", creature="baby dragon", place="mountain village")
    story, audio = generate_story_with_audio(prompt, audio_enabled=True)
    print("\nGenerated story:\n")
    print(story)
    if audio:
        print(f"\nAudio saved at: {audio}")
