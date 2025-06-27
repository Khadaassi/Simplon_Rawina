import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "tMyQcCxfGDdIt7wJ2RQw")

AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../App/media/generated_audios"))
os.makedirs(AUDIO_DIR, exist_ok=True)

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_audio(story_text, filename="output_audio.mp3"):
    """
    Generate an audio file from a given story text and return its relative path.
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("Missing ElevenLabs API key")

    output_path = os.path.join(AUDIO_DIR, filename)

    audio_stream = client.text_to_speech.convert(
        voice_id=DEFAULT_VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=story_text
    )

    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return os.path.join("generated_audios", filename)

if __name__ == "__main__":
    text = "Once upon a time, a little squirrel named Léo loved climbing trees in the magical forest."
    path = generate_audio(text, filename="leo_story.mp3")
    print(f"Generated audio: {path}")
