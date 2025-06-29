# Rawina

Rawina is a web application that automatically generates short illustrated and narrated stories for children aged 6–10, based on guided prompts and customizable themes.

This project was built as part of a learning module on natural language processing (NLP), integrating both backend and frontend technologies along with image and audio generation.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Setup](#setup)
* [Environment Variables](#environment-variables)
* [How It Works](#how-it-works)
* [Dockerization](#dockerization)
* [License](#license)
* [Authors](#authors)

---

## Overview

Rawina allows users to create short stories based on a selected theme. After answering a few guided questions, the application generates a complete narrative in French, with optional illustrations and narration.

Users can:

* Create and save stories
* Download them as PDF
* Listen to the narration (via ElevenLabs)
* View illustrations (generated with DALL·E or Pixabay)

---

## Features

* User authentication
* Guided prompt form for character and theme
* Text generation using GPT-2
* Image generation (Pixabay / DALL·E)
* Voice narration using ElevenLabs API
* Downloadable story (text + image + audio)
* Clean responsive UI using TailwindCSS

---

## Tech Stack

* **Backend:** Django, FastAPI
* **Frontend:** Django Templates + TailwindCSS
* **Model:** GPT-2 (fine-tuned)
* **Image:** DALL·E or Pixabay API
* **Audio:** ElevenLabs API
* **Deployment:** (to be defined)
* **Others:** dotenv, torch, transformers

---

## Project Structure

```
Simplon_Rawina/
├── App/                   # Django project
│   ├── users/             # Auth system
│   ├── stories/           # Story generation logic
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   └── settings.py
│
├── Model/                # ML and generation logic
│   ├── generator.py       # Text generation
│   ├── image_generator.py # Image generation
│   └── audio_generator.py # Audio narration
│
├── Api/                  # FastAPI app
│   └── main.py           # Endpoint for model
│
├── media/                # Generated images and audios
├── requirements.txt
└── README.md
```

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Khadaassi/Simplon_Rawina.git
cd Simplon_Rawina
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations and start Django:

```bash
python manage.py migrate
python manage.py runserver
```

5. Start the FastAPI model (in another terminal):

```bash
cd Api
uvicorn main:app --reload
```

---

## Environment Variables

Create a `.env` file in the root directory with the following:

```
ELEVENLABS_API_KEY=your_api_key
ELEVENLABS_VOICE_ID=your_voice_id (optional)
OPENAI_API_KEY=your_openai_key (if using DALL·E)
```

---

## How It Works

1. The user selects a theme and provides character details via form.
2. The Django app calls the FastAPI endpoint to generate the story.
3. If requested, illustrations and narration are generated.
4. The story is saved to the database with optional media.
5. The user can access a list of stories, read them, and download them.

---

## Dockerization

Dockerization

Both the Django application and the FastAPI service are containerized using Docker. Each component has its own Dockerfile, and a docker-compose.yml file orchestrates the services.

You will find:

One Dockerfile in App/ to containerize the Django backend.

One Dockerfile in Api/ to containerize the FastAPI-based text generation API.

A docker-compose.yml file at the project root to run both services together.

```bash
docker-compose up --build
```

This will start:

* Django server
* FastAPI service
* Any necessary dependencies

---

## License

This project is part of a Simplon AI/ML training course and is provided for educational purposes.

---

## Authors

* [Khadija Aassi](https://github.com/Khadaassi)
* [Raouf Addeche](https://github.com/RaoufAddeche)
