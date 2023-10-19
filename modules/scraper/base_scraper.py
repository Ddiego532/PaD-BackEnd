from util import create_conn, get_base_url, is_valid, is_absolute
from bs4 import BeautifulSoup
import criterias

# we only allocate it for one time.
EMPTY_LIST = []

class JSONCreator:
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

        # identifier handler.
        self.id = criteria.get("id", None)
        self._has_id = True

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
    
    def create_json_file(self):
        pass

    # force to go to a single url.
    def __connect_and_add_sublinks(self, url : str):
        print("Passed URL: ", url)
        conn = create_conn(url, self.conn_delay)
        soup = BeautifulSoup(conn.content, "html.parser")

        element = soup.find(self.target_tag, {"id" if self._has_id else "class": self.id})
    
        for link in element.find_all("a"):
            href = link.get("href")

            # has weird paths.
            if (href is None) or self.is_forbidden_sublink(href): 
                print("HREF NULL or FORBIDDEN: ", href)
                continue

            if not is_absolute(href):
                print("NOT ABSOULUTE: ", href)
                href = f"{self.seed_url}{href}"
            
            # doesn't match with the seed url.
            if not self.is_valid_sublink(href): 
                print("URL is not valid according to the seed: ", href)
                continue

            self.cached_links.add(href)

    def get_sublinks_singlepage(self):
        return self.__connect_and_add_sublinks(self.url)

    # this could vary in terms of fetching.
    # TODO: Implement it for another news sites.
    def get_links_by_exploring(self, max_level : int = 1):
        explore_path = self.__criteria.get("explore_path", None)
    
        if explore_path is None: 
            return self.get_sublinks_singlepage()
        
        # below 1 bad!!!
        max_level = max(max_level, 1)

        print(self.seed_url, explore_path)
        fullpath = f"{self.seed_url}/{explore_path}"

        for i in range(1, max_level + 1):
            numpath = fullpath.replace("page_num", str(i), 1)
            print("Going to: ", numpath)
            self.__connect_and_add_sublinks(numpath)

    def get_news_links(self):
        return self.cached_links
        
    def get_links_by_sitemap(self):
        sitemap = self.get_sitemaps()
        if not sitemap: return

    def get_sitemaps(self):
        # can return none.
        return self.__robot_parser.get_sitemaps()

LATERCERA_CRIT = criterias.LATERCERA
BIOBIO = criterias.BIOBIOCHILE

# we prolly not need these, these are needed when they are special cases.
latercera = BaseScrapper(criterias.MEGANOTICIAS)
latercera.get_links_by_exploring(10)

cached = latercera.get_news_links()

print(cached, len(cached))

# latercera.get_sublinks_singlepage()