# Model/train_model.py

from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_from_disk
import torch
import os

MODEL_NAME = "gpt2-large"
OUTPUT_DIR = "Model/fine_tuned_en"
DATASET_PATH = "Data/processed_dataset_en"

# Chargement du dataset
dataset = load_from_disk(DATASET_PATH)

# Tokenizer + modèle
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Tokenisation
def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])

# Collator pour le langage causal (GPT)
collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Configuration d’entraînement
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    per_device_train_batch_size=2,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="logs",
    logging_steps=10,
    fp16=torch.cuda.is_available(),  # accélère si GPU dispo
)

# Trainer Hugging Face
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=collator,
)

# Lancement de l'entraînement
trainer.train()

# Sauvegarde du modèle fine-tuné
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"✅ Model fine-tuned and saved in {OUTPUT_DIR}")
