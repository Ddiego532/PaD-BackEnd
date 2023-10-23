from helpers import create_session, handle_session, get_base_url
from scrapper_data import RobotsParser, NewsSaver, BeautifulSoup
from scraper_constants import EMPTY_LIST

# PARENT CLASS.
class BaseScraper:
    def __init__(self, criteria : dict) -> None:
        # private thing as we are scraping based on this.
        # protected as childs require it.
        self._criteria = criteria
        self.url = criteria.get("url", None)

        self.conn_delay = 0

        # should be like latercera.cl/
        self.seed_url = get_base_url(self.url)

        # try catch goofy aaa thing.
        if self.seed_url is None:
            raise ValueError(f"The seed URL has a null value.")
        

        self.page_session = create_session()
        self.cached_links = set()

        # imagine using this, but we are doing it for the xml.
        self.__robot_parser = RobotsParser(self.seed_url, self.page_session)
        self.news_saver = NewsSaver(self._criteria["news_selector"],  self.seed_url)

    def set_connection_delay(self, delay : int):
        self.conn_delay = delay
    
    def is_forbidden_sublink(self, link : str):
        forbidden_paths = self._criteria.get("forbidden_paths", EMPTY_LIST)
    
        return any(path in link for path in forbidden_paths)
    
    def handle_page_session(self, url : str, mode : str = "get", **kwargs):
        return handle_session(self.page_session, url=url, delay=self.conn_delay, mode=mode, **kwargs)

    def save_news(self):
        news_link : str

        for news_link in self.cached_links:
            conn = self.handle_page_session(url=news_link)
            if not conn: continue

            self.news_saver.save_to_dict(conn)

        print("Finished saving news in memory.")

    def get_news_saver(self):
        return self.news_saver

    # force to go to a single url.
    def _connect_and_add_sublinks(self, url : str):
        pass

    def get_sublinks_singlepage(self):
        return self._connect_and_add_sublinks(self.url)

    # this could vary in terms of fetching.
    # TODO: Implement it for another news sites.
    def get_links_by_exploring(self, max_level : int = 1):
        pass

    def start_scraping(self, level : int = 1):
        self.get_links_by_exploring(level)
        self.save_news()

    def get_news_links(self):
        return self.cached_links
        
    def get_links_by_sitemap(self):
        pass

    def get_sitemaps(self):
        # can return none.
        return self.__robot_parser.get_sitemaps()