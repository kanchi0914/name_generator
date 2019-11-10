import numpy as np
import requests
from googletrans import Translator

result = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=1000").json()
print(result[0])

#translated = result[0][""]
