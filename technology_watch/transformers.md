# Veille technique : Modèles Transformers, architecture de BERT et mécanisme d’attention

## 1. Introduction

Les modèles Transformers ont transformé en profondeur le traitement automatique du langage naturel (NLP). Introduits par Vaswani et al. en 2017 avec le papier *"Attention is All You Need"*, ils ont remplacé les architectures récurrentes (RNN, LSTM) grâce à leur parallélisation et leur capacité à capturer des dépendances à long terme.

Parmi ces modèles, BERT (Bidirectional Encoder Representations from Transformers), développé par Google AI, est devenu une référence incontournable pour de nombreuses tâches de NLP.

---

## 2. Le mécanisme d’attention

### Objectif

Le mécanisme d’attention permet à chaque mot d’une séquence de prêter attention à tous les autres, afin de capter les relations contextuelles, quel que soit leur éloignement dans la phrase.

### Fonctionnement : Self-Attention

Pour chaque mot, on calcule trois vecteurs :

- **Query (Q)** : ce que le mot cherche à comprendre
- **Key (K)** : la signature d’un mot pour être reconnu
- **Value (V)** : l’information contenue dans le mot

La formule de l’attention est :

````
Attention(Q, K, V) = softmax(QKᵀ / √d_k) × V
````


- `QKᵀ` calcule la similarité entre les mots
- La division par `√d_k` stabilise les gradients
- La softmax applique un poids à chaque mot en fonction de sa pertinence
- Le produit final donne une représentation enrichie du mot initial

### Avantages

- Traitement en parallèle (contrairement aux RNN)
- Capacité à modéliser les dépendances longues
- Base du succès des modèles comme GPT, BERT, T5, etc.

---

## 3. Architecture du Transformer

L’architecture se compose de deux blocs principaux : encodeur et décodeur. 

### Encodeur

Chaque couche de l’encodeur contient :

- Une couche de self-attention multi-têtes
- Un réseau feedforward (deux couches linéaires avec activation)
- Des connexions résiduelles et une normalisation

Les entrées sont des embeddings de mots auxquels on ajoute des **embeddings positionnels**, pour donner un sens à l’ordre.

### Décodeur

Similaire à l’encodeur, mais avec une attention supplémentaire :

- Une attention masquée pour générer un mot à la fois
- Une cross-attention qui interagit avec la sortie de l’encodeur

**Remarque** : BERT utilise uniquement l’encodeur.

---

## 4. Architecture de BERT

### Objectif

BERT est un modèle bidirectionnel : il lit une phrase dans les deux sens à la fois, ce qui améliore la compréhension du contexte.

### Détails techniques

- Basé uniquement sur l’encodeur du Transformer
- Deux variantes principales :
  - `bert-base` : 12 couches, 12 têtes, 110M de paramètres
  - `bert-large` : 24 couches, 16 têtes, 340M de paramètres

### Méthodes d’entraînement

1. **Masked Language Modeling (MLM)**  
   On masque aléatoirement 15 % des mots et le modèle doit les deviner.

2. **Next Sentence Prediction (NSP)**  
   Le modèle doit prédire si une phrase B suit logiquement une phrase A.

---

## 5. Cas d’usage de BERT

- Classification de texte (avis, spam, sujets)
- Analyse de sentiments
- Reconnaissance d’entités nommées (NER)
- Question-answering (ex : SQuAD)
- Résumé de texte, détection d’émotions (via variantes comme RoBERTa, T5)

---

## 6. Évolutions récentes et perspectives

- **Distillation** : création de versions plus légères (DistilBERT, TinyBERT)
- **Modèles spécialisés** : CamemBERT (français), BioBERT (domaine médical)
- **Modèles multilingues et multimodaux** : M-BERT, CLIP, Flamingo
- **Nouvelles approches** : In-context learning avec GPT, fine-tuning plus ciblé

---

## 7. Ressources complémentaires

- Article original : *Attention is All You Need* (Vaswani et al., 2017)
- Article BERT : *BERT: Pre-training of Deep Bidirectional Transformers* (Devlin et al., 2018)
- Hugging Face : [https://huggingface.co/models](https://huggingface.co/models)
- Visualisation interactive du Transformer :  
  [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
