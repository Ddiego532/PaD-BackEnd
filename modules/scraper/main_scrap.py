from base_scraper import BaseScraper
from criterias import *

# is there something more we can do?
class HTMLScrapper(BaseScraper):
    def __init__(self, criteria: dict) -> None:
        super().__init__(criteria)

        self.target_tag = criteria.get("tag", None)

    def get_links_by_exploring(self, max_level: int = 1):
        explore_path = self._criteria.get("explore_path", None)
    
        if explore_path is None: 
            return self.get_sublinks_singlepage()
        
        # below 1 bad!!!
        max_level = max(max_level, 1)

        print(self.seed_url, explore_path)
        fullpath = f"{self.seed_url}/{explore_path}"

        for i in range(1, max_level + 1):
            numpath = fullpath.replace("page_num", str(i), 1)
            print("Going to: ", numpath)
            self._connect_and_add_sublinks(numpath)

        return super().get_links_by_exploring(max_level)

scrap = HTMLScrapper(TVN_NOTICIAS)
scrap.get_links_by_exploring(1)

print(scrap.get_news_links(), len(scrap.get_news_links()))

scrap.save_news()