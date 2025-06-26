import os
import re
import requests
import openai
from datetime import datetime
from dotenv import load_dotenv

# === Chargement des variables d'environnement ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Répertoire de sortie pour les images ===
IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../App/media/images"))
os.makedirs(IMAGE_DIR, exist_ok=True)


# === Génération d'une image via DALL·E 3 ===
def generate_image(prompt, filename_prefix="scene"):
    """
    Génère une image avec DALL·E 3 et l'enregistre localement.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(IMAGE_DIR, filename)

    try:
        print(f"🎨 Génération d'une image pour : {prompt}")
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url

        image_data = requests.get(image_url)
        with open(filepath, "wb") as f:
            f.write(image_data.content)

        print(f"✅ Image sauvegardée : {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Erreur lors de la génération d'image : {e}")
        return None

# === Génération d'une seule image type couverture ===
def generate_cover_image(story_text, base_character, user_id="story"):
    """
    Génère une image unique représentative de toute l'histoire.
    """
    summary_prompt = f"Children's book cover illustration, soft pastel style, consistent characters, 3 to 6 years old style, {base_character} in the story: {story_text[:400]}"
    return generate_image(summary_prompt, filename_prefix=f"{user_id}_cover")

# === Pipeline principal : histoire → 1 image ===
def generate_images_for_story(story_text, user_id="story", base_character="a little animal"):
    """
    Génère une seule image représentative de toute l'histoire.
    """
    image_paths = []
    path = generate_cover_image(story_text, base_character, user_id)
    if path:
        image_paths.append(path)
    return image_paths

# === Test local ===
if __name__ == "__main__":
    test_story = (
        "Once upon a time, Luna was a little cat who lived in a blue house. "
        "One day, she met a big grey cat named Tom. "
        "They played with butterflies under the trees. "
        "Then they found a glowing cave. Inside, a wise owl greeted them. "
        "They returned home with glowing feathers and happy hearts."
    )
    images = generate_images_for_story(test_story, user_id="luna_test", base_character="a little cat")
    print("Images générées :")
    for img in images:
        print(" -", img)
