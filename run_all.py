import os

#Archivo encargado de ejecutar todo de forma secuencial, scrapeo, indexado y ranking.

def ejecutar_archivo(ruta):
    try:
        os.system(f"python {ruta}")
    except Exception as e:
        print(f"Error al ejecutar {ruta}: {str(e)}")

if __name__ == "__main__":
    carpetas_y_archivos = [
        "scraper/main_scraper.py",
        "scraper/normalize_scraper.py",
        "indexacion/json_to_txt.py",
        "indexacion/mapreduce.py",
        "ranking/doc_len.py"
    ]

    for archivo in carpetas_y_archivos:
        ruta_completa = os.path.join(os.path.dirname(__file__), archivo)
        ejecutar_archivo(ruta_completa)
