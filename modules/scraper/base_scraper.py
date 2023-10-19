from util import create_conn, get_base_url, is_valid, is_absolute
from bs4 import BeautifulSoup
import criterias

# we only allocate it for one time.
EMPTY_LIST = []

class NewsSaver:
    pass

# basically a robots.txt checker.
class RobotsParser:
    def __init__(self, url):
        self.__base_url = url
        # self.disallowed_links : list = None
        self.site_data = {}
        self.__request_data()

    def __request_data(self) -> None:
        robots_txt = create_conn(f"{self.__base_url}/robots.txt", 0)

        # FIXME: There are some sites without this file, so we need to add a better check.
        if not robots_txt:
            raise Exception("Can't fetch robots.txt")
        
        text_content = robots_txt.text
        stripped_newlines = text_content.splitlines()

        for data in stripped_newlines:
            # no need to iterate.
            if len(data) <= 0 or data.startswith("#"): continue

            # split one only.
            mapped = data.split(":", 1)

            # this is the thing we need.
            key = mapped[0]

            # we don't care about this.
            if key == "Allow": continue
            value = mapped[1].strip()

            if not key in self.site_data:
                self.site_data[key] : list = []

            self.site_data[key].append(value)

    def get_disallowed_links(self) -> list:        
        return self.site_data.get("Disallow", None)
    
    def get_sitemaps(self) -> list:
        return self.site_data.get("Sitemap", None)
    
    def get_user_agents(self) -> list:
        return self.site_data.get("User-agent", None)
    
    def get_site_data(self) -> dict:
        return self.site_data


class BaseScrapper:
    def __init__(self, criteria : dict) -> None:
        # private thing as we are scraping based on this.
        # protected as childs require it.
        self.__criteria = criteria
        self.url = criteria.get("url", None)
        self.target_tag = criteria.get("tag", None)

        self.conn_delay = 0

        self.id = criteria.get("id", None)

        if self.id is None:
            self.id = criteria.get("class", None)
            self._has_id = False

        # should be like latercera.cl/
        self.seed_url = get_base_url(self.url)

        # try catch goofy aaa thing.
        if self.seed_url is None:
            raise ValueError(f"The seed URL has a null value.")
        
        # imagine using this, but we are doing it for the xml.
        self.__robot_parser = RobotsParser(self.seed_url)
        self.cached_links = set()

    def set_connection_delay(self, delay : int):
        self.conn_delay = delay

    def is_valid_sublink(self, link : str):
        return is_valid(link, self.seed_url)
    
    def is_forbidden_sublink(self, link : str):
        forbidden_paths = self.__criteria.get("forbidden_paths", EMPTY_LIST)
    
        for path in forbidden_paths:
            if path in link:
                return True
            
        return False
    # this could vary in terms of fetching.
    # we don't need recursion.
    def get_links_by_soup(self, max_level : int = 1):
        conn = create_conn(self.url, self.conn_delay)
        soup = BeautifulSoup(conn.content, "html.parser")
        # the important part.
        element = soup.find(self.target_tag, {"id" if self._has_id else "class": self.id})
        
        for link in element.find_all("a"):
            href = link.get("href")

            # has weird paths.
            if (href is None) or self.is_forbidden_sublink(href): continue

            if not is_absolute(href):
                href = f"{self.seed_url}{href}"
            
            # doesn't match with the seed url.
            if not self.is_valid_sublink(href): continue

            print(href)

            # only news.

    def get_links_by_sitemap(self):
        sitemap = self.get_sitemaps()
        if not sitemap: return
        


    def find_news(self):
        pass

    def start_scraping(self):
        pass

    def get_sitemaps(self):
        # can return none.
        return self.__robot_parser.get_sitemaps()

LATERCERA_CRIT = criterias.LATERCERA
BIOBIO = criterias.BIOBIOCHILE

# we prolly not need these, these are needed when they are special cases.
class LaTerceraScrapper(BaseScrapper):
    def __init__(self) -> None:
        super().__init__(LATERCERA_CRIT)

class BioBioScrapper(BaseScrapper):
    def __init__(self):
        super().__init__(BIOBIO)

cnnscrapper = BaseScrapper(criterias.CNNCHILE)
cnnscrapper.get_links_by_soup()

biobio = BioBioScrapper()
biobio.get_links_by_soup()