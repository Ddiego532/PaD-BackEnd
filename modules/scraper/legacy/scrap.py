import requests
import json
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from scrapper_obj import Scrapper

nltk.download('punkt')
nltk.download('stopwords')

noticias = [ ]
cuerpos_noticias = [ ]
palabras_indices = {}
stop_words = set(stopwords.words('spanish'))

# I like this way.
ADITIONAL_STOPWORDS = [".", ",", ":", "“", "”", "*", "(", ")", "|", "biobiochile"]

for sw in ADITIONAL_STOPWORDS:
    stop_words.add(sw)

BIOBIO_LINK = 'https://www.biobiochile.cl/lista/categorias/nacional'
sc = Scrapper(BIOBIO_LINK)

for news in sc.get_news_on_articles():
    cuerpos_noticias.append(news)

palabras_clave_por_texto = []

for i, texto in enumerate(cuerpos_noticias):
    palabras = word_tokenize(texto.lower())
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    
    for palabra in palabras_filtradas:
        if palabra not in palabras_indices:
            palabras_indices[palabra] = [i]
        else:
            palabras_indices[palabra].append(i)
    
for palabra, indices in palabras_indices.items():
    print(f"'{palabra}': {indices}")
'''
for texto in cuerpos_noticias:
    
    palabras = word_tokenize(texto.lower())  

    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words ]

    frecuencia = FreqDist(palabras_filtradas)

    palabras_clave = frecuencia.most_common(3)  
    palabras_clave_por_texto.append(palabras_clave)


for i, palabras_clave in enumerate(palabras_clave_por_texto):
    print(f"Palabras clave noticia {i + 1}: {palabras_clave}")'''