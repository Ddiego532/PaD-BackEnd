import json
import re

# Rutas de entrada y salida
json_path = r"scraper/output_data/all_news.json"
output_txt_path = "indexacion/data/all_content.txt"

# Cargar el JSON desde el archivo
with open(json_path, "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

# Abrir el archivo de salida en modo escritura
with open(output_txt_path, "w", encoding="utf-8") as output_file:

    regex_pattern = re.compile(r'\s+')
    # Escribir el texto de la clave "content" en el archivo
    for item in json_data:
        content_text = regex_pattern.sub(' ', item["content"])
        output_file.write(content_text.strip() + "\n")

print(f"Contenido escrito en {output_txt_path}.")
