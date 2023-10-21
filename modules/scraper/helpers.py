from requests import get as req_get, post as req_post, exceptions
from urllib.parse import urlparse, urljoin
from time import sleep

# define constants.
SUCCESFUL_CODE = 200
HEADERS = {
    "Content-type": "text/html; charset=utf-8"
}

# Can return none.
# URL can't be empty.
# TODO: Add POST requests.
def create_conn(url : str, delay : float = 0):
    try:
        conn = req_get(url, headers=HEADERS)
        
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

#### BEAUTIFUL SOUP CRITERIA HELPERS #########
def get_element_by_id_or_class(data : dict, soup):
    id, has_id = data.get("id", None), True

    if id is None:
        id, has_id = data.get("class", None), False
    
    return soup.find(data["tag"], {"id" if has_id else "class": id})

def get_tag(data : dict, soup):
    # parents can give the way we retrieve the data.
    parent_data = data.get("parent", None)

    if parent_data is None:
        return get_element_by_id_or_class(data, soup)

    parent_element = get_element_by_id_or_class(parent_data, soup)
    first = parent_element.find(data["tag"])

    if first is not None:
        return first
    
    # worst case.
    return None