import os
import re

def check_word(palabra):
    if re.search("^[a-z0-9]+$", palabra):
        return palabra
    else:
        return ""

def main():
    path = r"../indexacion/reduced/all_content_reduced.txt"
    output_path = r"data/doclen.txt"

    with open(path, "r") as archivo:
        with open(output_path, "w") as output_file:
            for num_linea, linea in enumerate(archivo, start=1):
                palabras = linea.lower().split()
                document_len = sum(1 for palabra in palabras if len(check_word(palabra)) > 0)
                
                # Escribir la longitud de la línea en el archivo "doclen.txt"
                output_file.write(f"{document_len}\n")

if __name__ == "__main__":
    main()
