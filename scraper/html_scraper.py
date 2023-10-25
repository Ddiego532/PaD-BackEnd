from base_scraper import BaseScraper
from news_soup import NewsSoup
from helpers import is_valid, is_absolute

# is there something more we can do?
class HTMLScraper(BaseScraper):
    def __init__(self, criteria: dict) -> None:
        super().__init__(criteria)

        self.target_tag = criteria.get("tag", None)

    def _get_from_url(self):
        if not self._criteria.get("force_spec_url", False):
            return
        
        print("Connecting to the URL specified:", self.url)

        self._connect_and_add_sublinks(self.url)

    def get_links_by_exploring(self, max_level: int = 1):
        # only a hotfix for as.com
        self._get_from_url()

        explore_path = self._criteria.get("explore_path", None)
    
        if explore_path is None: 
            return self.get_sublinks_singlepage()
        
        # below 1 bad!!!
        max_level = max(max_level, 1)

        # print(self.seed_url, explore_path)
        fullpath = f"{self.seed_url}/{explore_path}"

        for i in range(1, max_level + 1):
            numpath = fullpath.replace("page_num", str(i), 1)
           #  print("Going to: ", numpath)
            self._connect_and_add_sublinks(numpath)

        return super().get_links_by_exploring(max_level)
    
    def _connect_and_add_sublinks(self, url: str):
        print("Passed URL: ", url)
        conn = self.handle_page_session(url=url)
        soup = NewsSoup(conn.text)

        element = soup.find_element_by_identifier_attribute(self._criteria)
    
        for link in element.find_all("a"):
            href = link.get("href")

            if (href is None) or self.is_forbidden_sublink(href): 
                continue

            if not is_absolute(href):
                href = f"{self.seed_url}{href}"
            
            # doesn't match with the seed url.
            if not is_valid(href, self.seed_url): 
                continue

            self.cached_links.add(href)