# Assuming we are only using the GET method.
from requests import get as req_get, post as req_post, exceptions
from urllib.parse import urlparse, urljoin
from time import sleep

# define constants.
SUCCESFUL_CODE = 200

# Can return none.
# URL can't be empty.
# TODO: Add POST requests.
def create_conn(url : str, delay : float = 0):
    try:
        conn = req_get(url)
        
        # give it a chance to avoid bans.
        if delay > 0:
            sleep(delay)

        # this is breaking the encapsulation logic, but we need to.
        # FIXME: Change it in some moment.
        if conn.status_code == SUCCESFUL_CODE:
            return conn
        
        print(f"The url: {url} returned {conn.status_code}")
    except exceptions.Timeout:
        print(f"The connection timed out for {url}")
    except exceptions.TooManyRedirects:
        print(f"The {url} has many redirections.")
    except exceptions.RequestException as err:
        print(f"Can't connect to {url}, because: {err}")

    return None

# TODO: Merge this.
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