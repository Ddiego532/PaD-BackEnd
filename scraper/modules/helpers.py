from requests import Session, exceptions
from urllib.parse import urlparse, urljoin
from time import sleep
from .constants import MAX_SPLITS_KEY_VALUES
import os
import json

# define constants.
# GET AND POST SUCCESS CODES.
SUCCESS_CODES = [200, 201]

def create_session():
    return Session()

# we only care about POST and GET.
def handle_session(sess : Session, url : str, delay : float = 0, mode : str = "get", **kwargs):
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
def is_absolute(url : str):
    return bool(urlparse(url).netloc)

# Check if its valid.
def is_valid(url, seed_url):
    return is_absolute(url) and get_base_url(url) == seed_url

def get_base_url(url : str):
    parse = urlparse(url)
    return f"{parse.scheme}://{parse.netloc}"

def get_joined_url(url, rel_path):
    return urljoin(url, rel_path)

def get_decoded_text(content : str):
    return content.encode("utf-8").decode("unicode-escape")

#### FILE SAVING HANDLING ######
def get_filename_by_domain(url : str):
    netloc = urlparse(url).netloc
    
    # replace dots with that because we don't want issues.
    return netloc.replace(".", "_")

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
# assuming we are inside of modules.
OUTPUT_PATH = os.path.join(os.path.dirname(FILE_PATH), "output_data")

def create_json_file(filename : str, data : any):
    # ensure that we are not having any issues.
    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    with open(os.path.join(OUTPUT_PATH, f"{filename}.json"), "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# WORKAROUND: This should be called when the json.loads fail!!!!!
def get_kv_by_string(search : str, string : str):
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