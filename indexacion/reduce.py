# Para ejecutar: python Map.py | python Reduce.py
# Imprime en un txt el resultado del map-reduce: palabra{index,cantidad}
# Tiene problemas con un input sucio, se cae en windows, muestra caracteres extranos en linux.

import sys
from collections import defaultdict
import unicodedata

def main():
    indice_invertido = defaultdict(lambda: defaultdict(int))

    for linea in sys.stdin:
        linea = unicodedata.normalize('NFKD', linea).encode('ascii','ignore').decode() # Normalizar la línea
        linea = linea.strip()
        if not linea:
            continue

        palabra, numero_linea = linea.split()
        numero_linea = int(numero_linea)

        indice_invertido[palabra][numero_linea] += 1

    reduced_path = r"indexacion/reduced/all_content_reduced.txt"   #Ruta de guardado.
    with open(reduced_path, 'w', encoding='utf-8') as f:
        for palabra in sorted(indice_invertido.keys()):
            lineas = indice_invertido[palabra]
            cantidad_pares = len(lineas)
            listado = "".join(

            # Separado por espacios               
                [f"{numero_linea} {conteo} " for numero_linea, conteo in lineas.items()])
            print(f"{palabra} {cantidad_pares} {listado}", file=f)

            # Con parentesis y comas
            #    [f"({numero_linea},{conteo})" for numero_linea, conteo in lineas.items()])
            #print(f"{palabra} {cantidad_pares}: {listado}", file=f)

if __name__ == "__main__":
    main()