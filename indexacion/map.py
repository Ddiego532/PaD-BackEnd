import re
import json

def quitar_tildes(texto):
    tildes = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "ü": "u", "Ü": "U"}
    return ''.join(tildes.get(letra, letra) for letra in texto)

def validar_palabra(palabra):
    patron = re.compile(r"^[a-zA-Z0-9áéíóúÁÉÍÓÚüÜ]+[.,]?$")
    palabra_sin_tilde = quitar_tildes(palabra)
    if patron.match(palabra_sin_tilde):
        return palabra_sin_tilde.rstrip(".,")  # Eliminar . o , al final
    else:
        return ""

def main():
    txt_path = r"data/all_content.txt"  # Ruta de lectura.
    with open(txt_path, "r", encoding="utf-8") as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            palabras = linea.lower().split()
            for palabra in palabras:
                palabra_valida = validar_palabra(palabra)
                if len(palabra_valida) > 0:
                    print(f"{palabra_valida} {num_linea}")

if __name__ == "__main__":
    main()