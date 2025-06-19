# # Model/image_generator.py

# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
# PIXABAY_URL = "https://pixabay.com/api/"

# def search_image_urls(query, num_images=1):
#     """
#     Recherche d'images sur Pixabay en fonction d'une requête textuelle.
#     Retourne une liste d'URLs d'images libres de droits.
#     """
#     if not PIXABAY_API_KEY:
#         raise ValueError("Clé API Pixabay non trouvée dans l'environnement")

#     # Nettoyage du texte : éviter les requêtes trop longues ou incohérentes
#     clean_query = " ".join(query.split()[:5])  # garder les 5 premiers mots max

#     params = {
#         "key": PIXABAY_API_KEY,
#         "q": clean_query,
#         "image_type": "photo",
#         "lang": "fr",
#         "per_page": num_images,
#         "safesearch": "true"
#     }

#     response = requests.get(PIXABAY_URL, params=params)
#     response.raise_for_status()
#     data = response.json()

#     return [hit["webformatURL"] for hit in data.get("hits", [])]

# # Exemple d'utilisation
# if __name__ == "__main__":
#     images = search_image_urls("renard magique aventure forêt", num_images=2)
#     print("\nImages trouvées :")
#     for img in images:
#         print(img)
