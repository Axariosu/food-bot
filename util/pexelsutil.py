from pexels_api import API
from dotenv import load_dotenv
import os


load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
api = API(PEXELS_API_KEY)
api.search('kitten', page=1, results_per_page=16)
photos = api.get_entries()
for photo in photos:
  # Print photographer
  print('Photographer: ', photo.photographer)
  # Print url
  print('Photo url: ', photo.url)
  # Print original size url
  print('Photo original size: ', photo.original)