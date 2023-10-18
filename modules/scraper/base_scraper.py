from util import create_conn, get_base_url, is_valid, is_absolute
from bs4 import BeautifulSoup
import criterias

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

    def is_valid_sublink(self, link : str):
        return is_valid(link, self.seed_url)

    def get_links(self):
        pass

    def find_news(self):
        pass

    def start_scraping(self):
        pass

    def is_valid_link(self):
        pass

    def should_connect(self, link : str):
        pass

    def get_sitemaps(self):
        # can return none.
        return self.__robot_parser.get_sitemaps()

LATERCERA_CRIT = criterias.LATERCERA
    
class LaTerceraScrapper(BaseScrapper):
    def __init__(self) -> None:
        super().__init__(LATERCERA_CRIT)

    def get_links(self):
        conn = create_conn(self.url, 0)
        soup = BeautifulSoup(conn.content, "html.parser")
        # the important part.
        element = soup.find(self.target_tag, {"id" if self._has_id else "class": self.id})
        
        for link in element.find_all("a"):
            href = link.get("href")

            if not is_absolute(href):
                href = f"{self.seed_url}{href}"

            if not self.is_valid_sublink(href): continue

            print(f"{href}")
        
latercera = LaTerceraScrapper()
print(latercera.get_sitemaps())
latercera.get_links()