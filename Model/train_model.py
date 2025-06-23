# Model/train_model.py

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from datasets import load_from_disk
import torch
import os

# 📁 Paramètres du projet
MODEL_NAME = "gpt2-large"
DATASET_PATH = "Data/processed_dataset_en"
OUTPUT_DIR = "Model/fine_tuned_en"

# 📦 Chargement du dataset
dataset = load_from_disk(DATASET_PATH)

# 🧠 Tokenizer et modèle
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # ✅ nécessaire pour éviter les erreurs de padding
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# 🧼 Tokenisation
def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])

# 📚 Collator pour du language modeling (GPT)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # ❌ Pas de masked language modeling pour GPT
)

# ⚙️ Configuration d'entraînement
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    per_device_train_batch_size=2,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="logs",
    logging_steps=10,
    fp16=torch.cuda.is_available(),  # ✅ accélère sur GPU compatible
)

# 🚀 Entraîneur Hugging Face
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

# ▶️ Entraînement
trainer.train()

# 💾 Sauvegarde du modèle
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"✅ GPT-2 Large fine-tuned and saved in {OUTPUT_DIR}")
