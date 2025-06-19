# Model/prepare_dataset.py

import json
from datasets import Dataset
import pandas as pd
import os

# Charger le fichier JSON déjà en anglais
with open("Data/histoires_combinees.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# On garde directement le champ "theme" et "story" tels quels
# On structure le texte d'entraînement pour GPT-2
examples = []
for entry in data:
    theme = entry["theme"]
    story_text = entry["story"]
    full_text = f"Theme: {theme}\nStory: {story_text}"
    examples.append({"text": full_text})

# Création du dataset Hugging Face
df = pd.DataFrame(examples)
dataset = Dataset.from_pandas(df)

# Sauvegarde
output_dir = "Data/processed_dataset_en"
os.makedirs(output_dir, exist_ok=True)
dataset.save_to_disk(output_dir)

print(f"✅ English dataset processed and saved to {output_dir}")
