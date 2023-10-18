from util import create_conn, get_base_url
from bs4 import BeautifulSoup

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


class NewsScrapper:
    def __init__(self, url : str) -> None:
        # should be like latercera.cl/
        self.seed_url = get_base_url(url)
        self.url = url

        # try catch goofy aaa thing.
        if self.seed_url is None:
            raise ValueError(f"The seed URL has a null value.")
        
        # imagine using this, but we are doing it for the xml.
        self.__robot_parser = RobotsParser(self.seed_url)

    def get_links(self):
        pass

    def find_news(self):
        pass

    def get_robots(self):
        return self.__robot_parser