from helpers import create_conn, get_element_by_id_or_class, get_tag, is_absolute
from scraper_constants import EMPTY_LIST
# only for fixing helpers args.
from bs4 import BeautifulSoup
import json

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

class NewsSaver:
    def __init__(self, crit : dict, source : str):
        self.news_selector = crit
        self.source = source
        self.saved_data = list()

    def set_filename(self):
        pass

    # retrieve this data first and then dump it.
    def save_to_dict(self, soup : BeautifulSoup):
        sel = self.news_selector
        text_data = sel["text_data"]

        # the stuff we save here.
        news_data = dict()

        # iterate the text stuff.
        for key in text_data:
            # special handler.
            # we dont care about these ones.
            value : dict = text_data[key]
            element = get_element_by_id_or_class(value, soup)
            news_data[key] = element.text.strip()

        # get the image.
        image = get_tag(sel["image_url"], soup)

        if image:
            # get source.
            source = image.get("src")

            if is_absolute(source):
                pass

            news_data["image"] = source

        # here we save the content.
        content = get_element_by_id_or_class(sel["content"], soup)
        ignorable_ids = sel.get("ignore_content_ids", EMPTY_LIST)
        content_text = ""

        for elem in content.findChildren():
            if elem is None: continue
            id = elem.get("id")
            class_id = elem.get("class")

            # ignorable tag, prolly ads related.
            if id in ignorable_ids or class_id in ignorable_ids: continue
            text : str = elem.text
        
            content_text += text

        # append this data to dictionary.
        news_data["content"] = content_text.strip()
        self.saved_data.append(news_data)

    def save_to_json(self, clear_data : bool = True):
        dump = json.dumps(self.saved_data, indent=4)
 
        with open("test.json", "w", encoding="utf-8") as json_file:
            json_file.write(dump)