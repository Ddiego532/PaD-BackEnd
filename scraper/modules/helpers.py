from requests import Session, exceptions
from urllib.parse import urlparse, urljoin
from time import sleep
import os
import json

# define constants.
# GET AND POST SUCCESS CODES.
SUCCESS_CODES = [200, 201]

# num of splits to do a key-value pair.
MAX_SPLITS_KEY_VALUES = 1

def create_session() -> Session:
    """
    Crea un objeto de tipo Session.

    :returns:
        sess : Session - La nueva sesión.
    """
    return Session()

# we only care about POST and GET.
def handle_session(sess : Session, url : str, delay : float = 0, mode : str = "get", **kwargs):
    """
    Maneja una sesion, a través de diferentes métodos.

    :params:
        sess : Session - El objeto Session.
        url : str - La URL a conectarse.
        delay : float - Tiempo de espera antes de poder realizar otra petición.
        mode : str - El método HTTP a utilizar, solamente soporta GET y POST.
        kwargs : vararg - Los argumentos para las funciones de get y post.

    :returns:
        resp : Response - La respuesta si la conexión tiene un código de conexión de exito.
    """
    try:
        connection = sess.get(url, **kwargs) if mode == "get" else sess.post(url, **kwargs)

        if delay > 0:
            sleep(delay)

        if connection.status_code in SUCCESS_CODES:
            return connection

        print(f"The url: {url} returned {connection.status_code}")
    except exceptions.Timeout:
        print(f"The connection timed out for {url}")
    except exceptions.TooManyRedirects:
        print(f"The {url} has many redirections.")
    except exceptions.RequestException as err:
        print(f"Can't connect to {url}, because: {err}")

    return None

###### URL PARSER HELPERS #########
def is_absolute(url : str) -> bool:
    """
    Revisa si una URL es relativa o absoluta.

    :returns:
        check : bool - La URL es absoluta.
    """
    return bool(urlparse(url).netloc)

# Check if its valid.
def is_valid(url, seed_url) -> bool:
    """
    Revisa si la URL es válida comparandola con la URL semilla.

    :returns:
        check : bool - La URL es válida.
    """
    return is_absolute(url) and get_base_url(url) == seed_url

def get_base_url(url : str):
    """
    Obtiene la URL base con su protocolo.

    :params:
        url : str - La URL.

    :returns:
        full_url : str - La URL base con su protocolo.
    """
    parse = urlparse(url)
    return f"{parse.scheme}://{parse.netloc}"

def get_joined_url(url, rel_path) -> str:
    """
    Une la URL con una ruta relativa.

    :params:
        url : str - La URL.
        rel_path : str - La ruta relativa.

    :returns:
        joined_url : str - La URL unida.
    """
    return urljoin(url, rel_path)

#### FILE SAVING HANDLING ######
def get_filename_by_domain(url : str) -> str:
    """
    Obtiene un nombre de archivo basado en un URL.

    :params:
        url : str - La URL.

    :returns:
        filename : str - Nombre de archivo apropiado para la URL.
    """
    netloc = urlparse(url).netloc
    
    # replace dots with that because we don't want issues.
    return netloc.replace(".", "_")

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
# assuming we are inside of modules.
OUTPUT_PATH = os.path.join(os.path.dirname(FILE_PATH), "output_data")

def create_json_file(filename : str, data : any):
    """
    Crea un archivo JSON.

    :params:
        filename : str - Nombre de archivo.
        data : any - Los datos a serializar en JSON.
    """
    # ensure that we are not having any issues.
    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    with open(os.path.join(OUTPUT_PATH, f"{filename}.json"), "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# WORKAROUND: This should be called when the json.loads fail!!!!!
def get_kv_by_string(search : str, string : str) -> str:
    """
    Obtiene un llave valor a través de un diccionario en formato string.

    :params:
        search : str - La llave a buscar.
        string : str - El diccionario en formato string.
    """
    stripped : list = string.splitlines()
    
    line : str
    for line in stripped:
        if "{" in line: continue
        if not ":" in line: continue

        mapped = line.split(":", MAX_SPLITS_KEY_VALUES)
        
        key = mapped[0]
        key = key.replace('"', '').strip()

        if key == search:
            return mapped[1]
        
    return None

def get_tags_from_str(content : str) -> list[str]:
    """
    Obtiene las etiquetas de una pagina en formato lista.

    :params:
        content : str - Las etiquetas separadas por comas.
    """
    # clean text.
    cleaned = content.strip()
    stripped = cleaned.split(",")
    return [word.lower() for word in stripped]