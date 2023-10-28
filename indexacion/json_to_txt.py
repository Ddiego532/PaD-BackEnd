import json

json_path = r"../scraper/output_data/all_news.json"
output_txt_path = "data/all_content.txt"

with open(json_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

if data and isinstance(data, list):
    contenidos = [entry.get("content", "") for entry in data]

    contenido_total = "\n".join(contenidos)

    with open(output_txt_path, "w", encoding="utf-8") as output_txt_file:
        output_txt_file.write(contenido_total)

    print("Contenidos extraídos y guardados en", output_txt_path)
else:
    print("El archivo JSON está vacío o no es una lista de objetos.")