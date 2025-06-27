import os
import re
import requests
import openai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../App/media/generated_images"))
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_image(prompt, filename_prefix="scene"):
    """
    Generate a single image with DALL·E 3 and return its relative path.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(IMAGE_DIR, filename)

    try:
        print(f"🎨 Generating image for: {prompt}")
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

        print(f"✅ Image saved: {filepath}")
        return os.path.join("generated_images", filename)

    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return None

def generate_cover_image(story_text, base_character, user_id="story"):
    """
    Generate a representative cover image for the entire story.
    """
    summary_prompt = f"Children's book cover illustration, soft pastel style, consistent characters, 3 to 6 years old style, {base_character} in the story: {story_text[:400]}"
    return generate_image(summary_prompt, filename_prefix=f"{user_id}_cover")

def generate_images_for_story(story_text, user_id="story", base_character="a little animal"):
    """
    Generate one representative image for the story.
    """
    image_paths = []
    path = generate_cover_image(story_text, base_character, user_id)
    if path:
        image_paths.append(path)
    return image_paths

if __name__ == "__main__":
    test_story = (
        "Once upon a time, Luna was a little cat who lived in a blue house. "
        "One day, she met a big grey cat named Tom. "
        "They played with butterflies under the trees. "
        "Then they found a glowing cave. Inside, a wise owl greeted them. "
        "They returned home with glowing feathers and happy hearts."
    )
    images = generate_images_for_story(test_story, user_id="luna_test", base_character="a little cat")
    print("Generated images:")
    for img in images:
        print(" -", img)
