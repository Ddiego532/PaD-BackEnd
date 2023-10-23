from requests import Session, exceptions
from urllib.parse import urlparse, urljoin
from time import sleep

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

#### BEAUTIFUL SOUP CRITERIA HELPERS #########
def get_element_by_identifier_attribute(data : dict, soup):
    id = data.get("identifier_attrib", None)

    if id is None:
        raise ValueError("Identifier can't be null.")
    
    id_value = data.get("attrib_value")

    return soup.find(data["tag"], {id : id_value})

def get_tag(data : dict, soup):
    # parents can give the way we retrieve the data.
    parent_data = data.get("parent", None)

    if parent_data is None:
        return get_element_by_identifier_attribute(data, soup)

    parent_element = get_element_by_identifier_attribute(parent_data, soup)

    # nested ahh thing
    if parent_element:
        first = parent_element.find(data["tag"])

        if first is not None:
            return first
        
    # no parent so use fallback.
    fallback_data = data.get("fallback", None)

    if fallback_data:
        fallback_tag = get_element_by_identifier_attribute(fallback_data, soup)

        print(fallback_tag.find(data["tag"]), "Xddddd")

        return fallback_tag.find(data["tag"])
    
    # worst case.
    return None

def are_elements_in_another_list(source_list : list, target_list: list):
    return any(elem in target_list for elem in source_list)

#### FILE SAVING HANDLING ######
def get_filename_by_domain(url : str):
    netloc = urlparse(url).netloc
    
    # replace dots with that because we don't want issues.
    return netloc.replace(".", "_")