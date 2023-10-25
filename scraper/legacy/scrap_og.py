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
ADITIONAL_STOPWORDS = [".", ",", ":", "“", "”", "*", "(", ")", "|"]

for sw in ADITIONAL_STOPWORDS:
    stop_words.add(sw)



link = 'https://www.biobiochile.cl/lista/categorias/nacional'

response = requests.get(link)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='UTF-8')

    article_elements = soup.find_all('article')

    for article in article_elements:
        a_element = article.find('a')

        if a_element:
            enlace = a_element.get('href')
            if enlace is not None:
               noticias.append(enlace)

    for url in noticias:
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                noticia = soup.find('article', {'class': 'post'})

                if noticia:
                    texto_noticia = noticia.get_text()
                    cuerpos_noticias.append(texto_noticia)

                    print(r'' + texto_noticia + '')
                else:
                    print("No se encontró el cuerpo de la noticia en el HTML.")
        else:
            print("Error al acceder a la página:", response.status_code)
            html = None
else:
    print(f'Error al cargar la página {url}: {response.status_code}')


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