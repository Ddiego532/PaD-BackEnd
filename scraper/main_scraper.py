from html_scraper import HTMLScraper
from modules.helpers import create_json_file
from criterias import *
import json
from translate import Translator
from textblob import TextBlob

EXAMPLE_LEVEL = 1
LIST_OF_SOURCES = [TELETRECE, ELDINAMO, ELMOSTRADOR, CNNCHILE, TVN_NOTICIAS,
                BIOBIOCHILE, LATERCERA, MEGANOTICIAS, ASCOM, COOPERATIVA, CHILEVISION]

#Se removio la fuente de ADN ya que daba problemas

print(len(LIST_OF_SOURCES))

ref_list = []

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

for webpage in LIST_OF_SOURCES:
    scrapper_obj = HTMLScraper(webpage)
    scrapper_obj.start_scraping()

    news_saver = scrapper_obj.get_news_saver()

    ref_list.extend(news_saver.get_saved_data())

for elemento in ref_list:
    titulo = elemento["title"]
    polaridad = analizar_polaridad(titulo)
    elemento["polarity"] = polaridad

create_json_file("all_news", ref_list)
