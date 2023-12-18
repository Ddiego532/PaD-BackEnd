import json
import re

def replace_special_characters(text):
    # Reemplazar caracteres especiales y tildes
    replacements = {
        'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'Ã±': 'ñ', 'Ã¼': 'ü', 'ã¡': 'á', 'ã©': 'é', 'ã­': 'í',
        'ã³': 'ó', 'ãº': 'ú', 'ã±': 'ñ', 'ã¼': 'ü', 'â': '“',
        'â': '”', 'â': '’', 'â': '–', 'â¢': '•', 'â': '–',
        'â¢': '•'
    }

    for search, replace in replacements.items():
        text = text.replace(search, replace)

    return text

def replace_special_characters_in_json(json_data):
    # Reemplazar caracteres especiales en el JSON
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, str):
                json_data[key] = replace_special_characters(value)
            elif isinstance(value, (list, dict)):
                replace_special_characters_in_json(value)
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            if isinstance(item, str):
                json_data[i] = replace_special_characters(item)
            elif isinstance(item, (list, dict)):
                replace_special_characters_in_json(item)

    return json_data

def main():
    # Lee el JSON desde un archivo (reemplaza 'nombre_del_archivo.json' con tu archivo JSON)
    input_path = r"scraper/output_data/pre_all_news.json" 
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Reemplaza caracteres especiales en el JSON
    replaced_data = replace_special_characters_in_json(data)

    # Guarda el JSON con caracteres reemplazados en otro archivo (reemplaza 'nombre_del_archivo_reemplazado.json')
    output_path = r"scraper/output_data/all_news.json" 
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(replaced_data, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
