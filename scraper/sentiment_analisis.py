import json
from translate import Translator
from textblob import TextBlob
import os

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
FILENAME = "all_news.json"
SCRAPPED_NEWS_PATH = os.path.join(os.path.dirname(FILE_PATH), "scraper", "output_data", FILENAME)

def analizar_polaridad(texto):
    # Crea un objeto Translator
    translator = Translator(to_lang="en", from_lang="es")

    # Realiza la traducción
    traduccion = translator.translate(texto)
    blob = TextBlob(traduccion)

    #Criterio para la polaridad [-1, -0,1[ = Negativo [-0,1 , 0,1] = Neutro ]0,1 , 1] = Positivo

    if blob.sentiment.polarity < -0.1:
        return "Negativo"
    elif -0.1 <= blob.sentiment.polarity <= 0.1:
        return "Neutro"
    else:
        return "Positivo"
    
with open(SCRAPPED_NEWS_PATH, "+r", encoding="utf-8") as json_file:
    noticias = json.load(json_file)

for elemento in noticias:
    titulo = elemento["title"]
    polaridad = analizar_polaridad(titulo)
    elemento["polarity"] = polaridad

with open(SCRAPPED_NEWS_PATH, 'w', encoding='utf-8') as file:
    json.dump(noticias, file, indent=2, ensure_ascii=False)