# Model/audio_generator.py

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "TxGEqnHWrfWFTfGW9XjX")  # Voix féminine douce par défaut
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_audio(story_text, filename="output_audio.mp3"):
    """
    Génère un fichier audio à partir d’un texte narratif.
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("Clé API ElevenLabs manquante")

    output_path = os.path.join(AUDIO_DIR, filename)

    audio_stream = client.text_to_speech.convert(
        voice_id=DEFAULT_VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=story_text
    )

    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return output_path

# Exemple d'utilisation
if __name__ == "__main__":
    texte = "Il était une fois un petit écureuil nommé Léo qui adorait grimper aux arbres de la forêt magique."
    path = generate_audio(texte, filename="leo_histoire.mp3")
    print(f"Audio généré : {path}")
