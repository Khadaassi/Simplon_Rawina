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

def build_prompt(name="Lina", creature="little owl", place="enchanted forest", theme="animals"):
    return (
        f"This is a short bedtime story for children aged 6 to 10.\n"
        f"Theme: {theme}\n"
        f"{name} is a {creature} who lives in a {place}. One day,"
    )
def clean_story(text, prompt):
    story = text.replace(prompt, "").strip()
    # Couper à la première apparition d’un saut de contexte
    for stop in ["Theme:", "Book", "Characters:", "Table of Contents"]:
        if stop in story:
            story = story.split(stop)[0].strip()
    return story


def is_story_valid(story, min_words=50):
    return len(story.split()) >= min_words

def generate_story(prompt, max_length=450, temperature=0.9, top_p=0.9, max_tries=3):
    encoded = tokenizer(prompt, return_tensors="pt", padding=True)
    input_ids = encoded["input_ids"]
    attention_mask = encoded["attention_mask"]

    for _ in range(max_tries):
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
        story = clean_story(story, prompt)
        if is_story_valid(story):
            return story

    return "Sorry, the story could not be generated correctly after several attempts."

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
    story = generate_story(prompt)
    print("\nGenerated story:\n")
    print(story)
    # if audio:
    #     print(f"\nAudio saved at: {audio}")
