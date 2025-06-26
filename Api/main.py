from fastapi import FastAPI
from pydantic import BaseModel
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

# === Chargement des variables d'environnement (.env) ===
load_dotenv()

# === Gestion de l'audio optionnelle ===
try:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from Model.audio_generator import generate_audio

    print("🔊 Module audio chargé avec succès.")
except ImportError:
    generate_audio = None
    print("⚠️ Module audio non disponible.")

# === Initialisation FastAPI ===
app = FastAPI()

# === Chargement du modèle et du tokenizer GPT2-XL ===
MODEL_PATH = Path(__file__).resolve().parent / "../Model/gpt2-xl-rawina"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH, local_files_only=True)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# === Schéma d'entrée JSON pour Postman ou frontend ===
class StoryRequest(BaseModel):
    user_id: str
    theme: str
    name: str
    creature: str
    place: str
    audio: bool = False

# === Prompt structuré ===
def build_prompt(name: str, creature: str, place: str, theme: str) -> str:
    return (
        "Write a short bedtime story for children aged 3 to 6 years old.\n"
        "The story must be gentle and simple.\n"
        f"Theme: {theme}\n"
        f"The main character is {name}, a {creature} who lives in a {place}.\n"
        "The story must start with: 'Once upon a time'.\n"
        "It must have a beginning, a middle, and an end.\n"
        "Write only one story.\n"
        "Now write the story:\n"
        f"Once upon a time, {name} was a {creature} who lived in a {place}. One day,"
    )

# === Nettoyage post-génération ===
def clean_story(text: str, prompt: str) -> str:
    story = text.replace(prompt, "").strip()
    stopwords = ["Once upon a time", "Theme:", "Example:", "Now write another", "Table of Contents", "Book", "Chapter"]
    for stop in stopwords:
        parts = story.split(stop)
        if len(parts) > 1:
            story = parts[0].strip()
    return story.strip()

# === Validation minimale (optionnelle) ===
def is_story_valid(story: str, min_words=50) -> bool:
    return len(story.split()) >= min_words and story.endswith(".")

# === Génération de l'histoire ===
def generate_story(prompt: str, max_length=400, temperature=0.8, top_p=0.95, max_tries=3) -> str:
    encoded = tokenizer(prompt, return_tensors="pt", padding=True).to(device)
    for _ in range(max_tries):
        output = model.generate(
            input_ids=encoded["input_ids"],
            attention_mask=encoded["attention_mask"],
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=1.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
        story = tokenizer.decode(output[0], skip_special_tokens=True)
        story = clean_story(story, prompt)
        return story
    return "Sorry, the story could not be generated correctly after several attempts."

# === Endpoint GET test ===
@app.get("/")
def root():
    return {"message": "Rawina Story Generator API is running."}

# === Endpoint POST principal ===
@app.post("/generate")
def generate(request: StoryRequest):
    prompt = build_prompt(
        name=request.name,
        creature=request.creature,
        place=request.place,
        theme=request.theme
    )

    print(f"📥 Requête reçue pour l'utilisateur : {request.user_id}")
    story = generate_story(prompt)
    audio_path = None

    if request.audio:
        print("🎧 Audio demandé")
        if generate_audio:
            try:
                filename = f"story_{request.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                audio_path = generate_audio(story, filename=filename)
                print(f"✅ Audio généré : {audio_path}")
            except Exception as e:
                print(f"❌ Erreur lors de la génération audio : {e}")
                audio_path = None
        else:
            print("⚠️ Module audio non chargé, audio ignoré.")

    return {
        "user_id": request.user_id,
        "story": story,
        "audio_path": audio_path
    }
