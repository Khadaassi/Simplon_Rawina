# def build_prompt(name="Lina", creature="little owl", place="enchanted forest", theme="Fantasy"):
#     return (
#         f"This is a short bedtime story for children aged 3 to 6.\n"
#         f"Theme: {theme}\n"
#         f"Starts with a character {name}, a creature type {creature}, and a place {place}.\n"
#         "Ends with a moral lesson.\n"
#         # f"{name} is a {creature} who lives in a {place}. One day,"
#     )


# def clean_story(text, prompt):
#     story = text.replace(prompt, "").strip()
#     # Couper à la première apparition d’un saut de contexte
#     for stop in ["Theme:", "Book", "Characters:", "Table of Contents"]:
#         if stop in story:
#             story = story.split(stop)[0].strip()
#     return story


# def is_story_valid(story, min_words=50):
#     return len(story.split()) >= min_words

# def generate_story(prompt, max_length=600, temperature=0.9, top_p=0.9, max_tries=3):
#     encoded = tokenizer(prompt, return_tensors="pt", padding=True)
#     input_ids = encoded["input_ids"]
#     attention_mask = encoded["attention_mask"]

#     for _ in range(max_tries):
#         output = model.generate(
#             input_ids=input_ids,
#             attention_mask=attention_mask,
#             max_length=max_length,
#             temperature=temperature,
#             top_p=top_p,
#             repetition_penalty=1.2,
#             do_sample=True,
#             pad_token_id=tokenizer.eos_token_id
#         )
#         story = tokenizer.decode(output[0], skip_special_tokens=True)
#         story = clean_story(story, prompt)
#         if is_story_valid(story):
#             return story

#     return "Sorry, the story could not be generated correctly after several attempts."

# def generate_story_with_audio(prompt, audio_enabled=False):
#     story = generate_story(prompt)
#     audio_path = None
#     if audio_enabled:
#         safe_filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
#         audio_path = generate_audio(story, filename=safe_filename)
#     return story, audio_path

# # Exemple d'utilisation
# if __name__ == "__main__":
#     prompt = build_prompt(name="Tilo", creature="Duck", place="farm", theme="adventure")
#     story = generate_story(prompt)
#     print("\nGenerated story:\n")
#     print(story)
#     # if audio:
#     #     print(f"\nAudio saved at: {audio}")


from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from datetime import datetime

# Gestion de l'audio optionnelle
try:
    from audio_generator import generate_audio
except ImportError:
    generate_audio = None

# === Configuration ===
MODEL_PATH = "./Model/gpt2-xl-rawina"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Chargement tokenizer + modèle ===
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
model.to(DEVICE)
model.eval()

# === Prompt encadré pour les enfants ===
def build_prompt(name="Lina", creature="little bunny", place="green meadow", theme="Friendship"):
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

# === Nettoyage du texte généré ===
def clean_story(text, prompt):
    story = text.replace(prompt, "").strip()
    stopwords = ["Once upon a time", "Theme:", "Example:", "Now write another", "Table of Contents", "Book", "Chapter"]
    for stop in stopwords:
        if stop in story:
            story = story.split(stop)[0].strip()
    # Nettoyage des répétitions de fin
    story = story.strip().rstrip(".") + "."
    if not story.endswith("The end."):
        story += " The end."
    return story

# === Validation stricte ===
def is_story_valid(story, min_words=50):
    return len(story.split()) >= min_words and "Once upon a time" in story and "The end." in story

# === Génération avec tentatives multiples ===
def generate_story(prompt, max_length=400, temperature=0.8, top_p=0.95, max_tries=3):
    encoded = tokenizer(prompt, return_tensors="pt", padding=True).to(DEVICE)

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
        # if is_story_valid(story):
        return story

    return "Sorry, the story could not be generated correctly after several attempts."

# === Audio (optionnel) ===
def generate_story_with_audio(prompt, audio_enabled=False):
    story = generate_story(prompt)
    audio_path = None
    if audio_enabled and generate_audio:
        filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        audio_path = generate_audio(story, filename=filename)
    return story, audio_path

# === Test CLI ===
if __name__ == "__main__":
    prompt = build_prompt(name="Tilo", creature="little duck", place="colorful farm", theme="Adventure")
    story, _ = generate_story_with_audio(prompt, audio_enabled=False)
    print("\nGenerated story:\n")
    print(story)
